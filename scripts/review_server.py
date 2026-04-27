from __future__ import annotations

import argparse
import json
import re
import sys
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


VALID_STATUSES = {"", "skip", "weak", "improving", "mastered"}
FEEDBACK_HEADING = {
    "weak": "New weak spots",
    "improving": "Strengthened topics",
    "mastered": "Newly mastered topics",
}


def find_workspace_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".interview").exists() and (parent / "interview-packs").exists():
            return parent
    raise RuntimeError("Could not locate workspace root from script path.")


ROOT = find_workspace_root()
INTERVIEW_DIR = ROOT / ".interview"
PACKS_DIR = ROOT / "interview-packs"
PROFILE_MEMORY_PATH = INTERVIEW_DIR / "profile-memory.md"
FEEDBACK_JSON_PATH = INTERVIEW_DIR / "feedback.json"
FEEDBACK_MD_PATH = INTERVIEW_DIR / "feedback.md"
REVIEW_HTML_PATH = INTERVIEW_DIR / "review-pack.html"


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def latest_pack_path() -> Path:
    candidates = sorted(PACKS_DIR.glob("pack-*.md"), key=lambda p: (p.stat().st_mtime, p.name), reverse=True)
    if not candidates:
        raise FileNotFoundError("No interview pack found under interview-packs/.")
    return candidates[0]


def list_pack_paths() -> list[Path]:
    return sorted(PACKS_DIR.glob("pack-*.md"), key=lambda p: (p.stat().st_mtime, p.name), reverse=True)


def find_pack_path(pack_id: str) -> Path:
    wanted = normalize_topic(pack_id)
    if not wanted:
        return latest_pack_path()
    for pack_path in list_pack_paths():
        if pack_path.stem == wanted:
            return pack_path
    raise FileNotFoundError(f"Pack not found: {pack_id}")


def compact(text: str) -> str:
    text = text.replace("\r\n", "\n").strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def extract_block(content: str, label: str) -> str:
    pattern = re.compile(
        rf"\*\*{re.escape(label)}\*\*\s*(.*?)(?=\n\*\*[^*]+\*\*|\Z)",
        re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        return ""
    return compact(match.group(1))


def parse_pack(pack_path: Path) -> dict:
    text = read_text(pack_path)
    section_matches = list(re.finditer(r"(?m)^## (\d+)\.\s+(.+)$", text))
    question_matches = list(re.finditer(r"(?m)^### Q(\d+)\.\s+(.+)$", text))
    sections: list[tuple[int, str]] = [(m.start(), m.group(2).strip()) for m in section_matches]
    items = []

    for index, match in enumerate(question_matches):
        start = match.start()
        end = question_matches[index + 1].start() if index + 1 < len(question_matches) else len(text)
        block = text[start:end].strip()
        question_id = f"Q{match.group(1)}"
        title = match.group(2).strip()
        section_title = "Unknown"
        for section_pos, section_name in sections:
            if section_pos < start:
                section_title = section_name
            else:
                break

        items.append(
            {
                "question_id": question_id,
                "title": title,
                "section": section_title,
                "question": extract_block(block, "Question"),
                "what_it_tests": extract_block(block, "What It Tests"),
                "one_minute_skeleton": extract_block(block, "One-Minute Skeleton"),
                "expanded_answer": extract_block(block, "Expanded Answer"),
                "possible_follow_ups": extract_block(block, "Possible Follow-Ups"),
            }
        )

    pack_id = pack_path.stem
    date_match = re.search(r"pack-(\d{4})(\d{2})(\d{2})$", pack_id)
    display_date = pack_id
    if date_match:
        display_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"

    return {
        "pack_id": pack_id,
        "pack_file": str(pack_path.relative_to(ROOT)).replace("\\", "/"),
        "display_date": display_date,
        "items": items,
    }


def load_feedback_store() -> dict:
    if not FEEDBACK_JSON_PATH.exists():
        return {"version": 1, "updated_at": None, "packs": {}}
    data = json.loads(read_text(FEEDBACK_JSON_PATH))
    data.setdefault("version", 1)
    data.setdefault("updated_at", None)
    data.setdefault("packs", {})
    return data


def merge_feedback(pack: dict, store: dict) -> dict:
    saved_pack = store.get("packs", {}).get(pack["pack_id"], {})
    saved_items = {item["question_id"]: item for item in saved_pack.get("items", [])}
    merged_items = []
    for item in pack["items"]:
        saved = saved_items.get(item["question_id"], {})
        merged_items.append(
            {
                **item,
                "status": saved.get("status", ""),
                "topic_label": saved.get("topic_label", item["title"]),
                "note": saved.get("note", ""),
            }
        )
    return {**pack, "items": merged_items}


def list_packs() -> list[dict]:
    packs = []
    for pack_path in list_pack_paths():
        pack = parse_pack(pack_path)
        packs.append(
            {
                "pack_id": pack["pack_id"],
                "pack_file": pack["pack_file"],
                "display_date": pack["display_date"],
            }
        )
    return packs


def normalize_topic(topic: str) -> str:
    return re.sub(r"\s+", " ", topic).strip()


def render_feedback_md(store: dict) -> str:
    lines = ["# Feedback Log", ""]
    packs = sorted(store.get("packs", {}).items(), key=lambda pair: pair[0], reverse=True)
    if not packs:
        lines.extend(["- No feedback has been saved yet."])
        return "\n".join(lines) + "\n"

    for pack_id, pack in packs:
        lines.append(f"## {pack_id}")
        lines.append(f"- Source pack: `{pack.get('pack_file', '')}`")
        lines.append(f"- Saved at: {pack.get('saved_at', '')}")
        for item in pack.get("items", []):
            status = item.get("status", "")
            if status not in {"weak", "improving", "mastered"}:
                continue
            lines.append(f"- {status}: {item.get('topic_label', item.get('title', ''))}")
            lines.append(f"  - question: {item.get('question_id', '')} {item.get('title', '')}")
            if item.get("note"):
                lines.append(f"  - note: {item['note']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_top_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    matches = list(re.finditer(r"(?m)^## .+$", text))
    if not matches:
        return text.strip(), []
    intro = text[: matches[0].start()].rstrip()
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = match.group(0).strip()
        body = text[start:end].strip("\n")
        sections.append((heading, body))
    return intro, sections


def parse_bullets(body: str) -> list[str]:
    return [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]


def unique_bullets(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        key = normalize_topic(value).casefold()
        if not value or key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def latest_feedback_topics(store: dict) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    pack_items: list[dict] = []
    packs = store.get("packs", {})
    for pack_id in sorted(packs.keys()):
        saved_at = packs[pack_id].get("saved_at", "")
        for item in packs[pack_id].get("items", []):
            topic = normalize_topic(item.get("topic_label", "") or item.get("title", ""))
            if not topic:
                continue
            pack_items.append(
                {
                    "topic": topic,
                    "status": item.get("status", ""),
                    "note": item.get("note", ""),
                    "saved_at": saved_at,
                }
            )
    pack_items.sort(key=lambda item: item["saved_at"])
    for item in pack_items:
        latest[item["topic"]] = item
    return latest


def render_recent_update(pack: dict, items: list[dict]) -> str:
    grouped = {"weak": [], "improving": [], "mastered": []}
    noted = []
    for item in items:
        status = item.get("status", "")
        topic = normalize_topic(item.get("topic_label", "") or item.get("title", ""))
        if status in grouped and topic:
            grouped[status].append(topic)
        if item.get("note"):
            noted.append(f"{topic}: {item['note']}")

    lines = [f"### {pack['display_date']} ({pack['pack_id']})"]
    for status in ("weak", "improving", "mastered"):
        lines.append(f"- {FEEDBACK_HEADING[status]}:")
        topics = unique_bullets(grouped[status])
        if topics:
            lines.extend([f"  - {topic}" for topic in topics])
        else:
            lines.append("  - None")
    lines.append("- Still needs practice:")
    weak_topics = unique_bullets(grouped["weak"])
    if weak_topics:
        lines.extend([f"  - {topic}" for topic in weak_topics])
    else:
        lines.append("  - None")
    if noted:
        lines.append("- Notes:")
        lines.extend([f"  - {note}" for note in unique_bullets(noted)])
    return "\n".join(lines)


def update_profile_memory(pack: dict, saved_items: list[dict], store: dict) -> None:
    if PROFILE_MEMORY_PATH.exists():
        text = read_text(PROFILE_MEMORY_PATH)
    else:
        text = "# Candidate Memory\n"

    intro, sections = parse_top_sections(text)
    section_map = {heading: body for heading, body in sections}
    order = [heading for heading, _ in sections]

    weak_heading = "## Repeated Weak Spots"
    mastered_heading = "## Mastered Topics"
    recent_heading = "## Recent Pack Updates"

    existing_weak = parse_bullets(section_map.get(weak_heading, ""))
    existing_mastered = parse_bullets(section_map.get(mastered_heading, ""))

    latest_topics = latest_feedback_topics(store)
    weak_topics = [topic for topic, item in latest_topics.items() if item.get("status") == "weak"]
    mastered_topics = [topic for topic, item in latest_topics.items() if item.get("status") == "mastered"]

    weak_topics = unique_bullets(existing_weak + weak_topics)
    mastered_topics = unique_bullets(existing_mastered + mastered_topics)

    weak_keys = {normalize_topic(item).casefold() for item in weak_topics}
    mastered_topics = [item for item in mastered_topics if normalize_topic(item).casefold() not in weak_keys]

    mastered_keys = {normalize_topic(item).casefold() for item in mastered_topics}
    weak_topics = [item for item in weak_topics if normalize_topic(item).casefold() not in mastered_keys]

    section_map[weak_heading] = "\n".join(f"- {item}" for item in weak_topics) if weak_topics else "- None"
    section_map[mastered_heading] = "\n".join(f"- {item}" for item in mastered_topics) if mastered_topics else "- None"

    existing_recent = section_map.get(recent_heading, "")
    _, recent_sections = parse_top_sections(existing_recent.replace("### ", "## ")) if existing_recent.strip() else ("", [])
    recent_map: dict[str, str] = {}
    if existing_recent.strip():
        recent_matches = list(re.finditer(r"(?m)^### .+$", existing_recent))
        for index, match in enumerate(recent_matches):
            start = match.end()
            end = recent_matches[index + 1].start() if index + 1 < len(recent_matches) else len(existing_recent)
            recent_map[match.group(0).strip()] = existing_recent[start:end].strip("\n")

    recent_title = f"### {pack['display_date']} ({pack['pack_id']})"
    recent_map[recent_title] = render_recent_update(pack, saved_items)[len(recent_title) :].strip("\n")
    ordered_recent_titles = [recent_title] + [title for title in recent_map.keys() if title != recent_title]
    section_map[recent_heading] = "\n\n".join(
        f"{title}\n{recent_map[title]}".rstrip() for title in ordered_recent_titles[:12]
    )

    for heading in (weak_heading, mastered_heading, recent_heading):
        if heading not in order:
            order.append(heading)

    parts = [intro.strip()] if intro.strip() else []
    for heading in order:
        parts.append(heading)
        parts.append(section_map.get(heading, "").strip())

    write_text(PROFILE_MEMORY_PATH, "\n\n".join(part for part in parts if part != "").rstrip() + "\n")


def save_feedback(payload: dict) -> dict:
    pack_id = payload.get("pack_id", "").strip()
    pack_file = payload.get("pack_file", "").strip()
    items = payload.get("items", [])
    if not pack_id or not pack_file or not isinstance(items, list):
        raise ValueError("Invalid payload.")

    normalized_items = []
    for item in items:
        status = item.get("status", "").strip()
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        title = item.get("title", "").strip()
        question_id = item.get("question_id", "").strip()
        topic_label = normalize_topic(item.get("topic_label", "").strip() or title)
        note = normalize_topic(item.get("note", "").strip())
        normalized_items.append(
            {
                "question_id": question_id,
                "title": title,
                "section": item.get("section", "").strip(),
                "topic_label": topic_label,
                "status": status,
                "note": note,
            }
        )

    store = load_feedback_store()
    now = datetime.now().isoformat(timespec="seconds")
    store["updated_at"] = now
    store["packs"][pack_id] = {
        "pack_file": pack_file,
        "saved_at": now,
        "items": normalized_items,
    }
    write_text(FEEDBACK_JSON_PATH, json.dumps(store, ensure_ascii=False, indent=2) + "\n")
    write_text(FEEDBACK_MD_PATH, render_feedback_md(store))
    pack = parse_pack(ROOT / pack_file)
    update_profile_memory(pack, normalized_items, store)

    counts = {"weak": 0, "improving": 0, "mastered": 0, "skip": 0}
    for item in normalized_items:
        if item["status"] in counts:
            counts[item["status"]] += 1
    return {"ok": True, "counts": counts, "saved_at": now}


class ReviewHandler(BaseHTTPRequestHandler):
    server_version = "ResumeInterviewPackReview/1.0"

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, content_type: str = "text/html; charset=utf-8") -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/review-pack.html"}:
            self._send_text(read_text(REVIEW_HTML_PATH))
            return
        if parsed.path == "/api/packs":
            try:
                self._send_json({"packs": list_packs()})
            except Exception as exc:  # noqa: BLE001
                self._send_json({"ok": False, "error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/state":
            try:
                query = parse_qs(parsed.query)
                pack_id = query.get("pack", [""])[0]
                pack_path = find_pack_path(pack_id) if pack_id else self.server.pack_path  # type: ignore[attr-defined]
                pack = merge_feedback(parse_pack(pack_path), load_feedback_store())
                self._send_json(pack)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"ok": False, "error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/save":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            result = save_feedback(payload)
            self._send_json(result)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"ok": False, "error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve an interactive interview-pack feedback page.")
    parser.add_argument("--pack", help="Path to a specific pack markdown file. Defaults to the latest pack.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    pack_path = Path(args.pack).resolve() if args.pack else latest_pack_path()
    if not pack_path.exists():
        print(f"Pack not found: {pack_path}", file=sys.stderr)
        return 1

    server = ThreadingHTTPServer((args.host, args.port), ReviewHandler)
    server.pack_path = pack_path  # type: ignore[attr-defined]
    url = f"http://{args.host}:{args.port}/review-pack.html"
    print(f"Serving feedback UI for {pack_path}")
    print(f"Open: {url}")
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:  # noqa: BLE001
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
