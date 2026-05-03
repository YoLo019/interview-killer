# Profile Schema

Use `.interview/profile.json` as the stable config file and `.interview/profile-memory.md` as the persistent derived memory.
Use `.interview/feedback.json` and `.interview/feedback.md` as explicit review feedback inputs.

## `profile.json`

Recommended shape:

```json
{
  "resume_path": "C:/path/to/resume.md",
  "projects": [
    {
      "name": "HappyFlow",
      "path": "D:/code/happyflow"
    }
  ],
  "materials": {
    "interview_notes": [
      "C:/path/to/interview-notes.md"
    ],
    "knowledge_bases": [
      "C:/path/to/agent-kb.md",
      "C:/path/to/rag-kb.md",
      "C:/path/to/prompt-harness-kb.md"
    ]
  }
}
```

Rules:

- `resume_path` should point to a readable Markdown or TXT file.
- `projects[].path` should point to the project directory that supports the matching resume project.
- `projects[].name` should match the project name used in the resume as closely as possible.
- `projects[].resume_claim` is optional. Add it only when the resume description is too short or you want the skill to defend a narrower project framing.
- `interview_notes` are style signals, not a raw bank of final questions.
- `projects[].path` is mainly used to ground answers, validate claims, and prepare realistic follow-ups. By default it should not become the primary source of main interview questions.
- `knowledge_bases` support answers for project, principle, engineering, and fundamentals sections.

## `profile-memory.md`

Recommended sections:

```md
# Candidate Memory

## Stable Profile
- Target role:
- Main stacks:
- Main claims to defend:

## Project Summaries
### Project: ...
- Resume claim if needed:
- Grounded summary:
- Key modules worth mentioning:
- Metrics or impact:
- Risks or weakly supported claims:

## Repeated Weak Spots
- ...

## Mastered Topics
- ...

## Historical Representative Questions
- ...

## High-Value Follow-Up Patterns
- ...

## AI Workflow Notes
- Daily AI usage:
- AI coding habits:
- Validation habits:
- Framework preferences:

## Recent Pack Updates
### 2026-04-26
- New weak spots:
- Strengthened topics:
- Newly mastered topics:
- Still needs practice:
```

Keep this file concise and evidence-oriented.  
Replace stale content on refresh instead of appending forever.
After each generated pack or clear answer review, refresh the weak spots, mastered topics, and recent pack updates sections instead of leaving them static.
Only mark a topic as mastered when it is grounded by repeated stable answers, project evidence, or explicit user confirmation.

## `feedback.json`

Recommended role:

- machine-readable review feedback collected after reading a generated pack
- per-question status such as `weak`, `improving`, `mastered`, or `skip`
- editable topic label for what should be written back into long-term memory
- optional freeform note

Recommended shape:

```json
{
  "version": 1,
  "updated_at": "2026-04-26T21:00:00",
  "packs": {
    "pack-20260426": {
      "pack_file": "interview-packs/pack-20260426.md",
      "saved_at": "2026-04-26T21:00:00",
      "items": [
        {
          "question_id": "Q1",
          "title": "HappyFlow ...",
          "section": "Project Deep Dive",
          "topic_label": "HappyFlow 项目归因边界",
          "status": "weak",
          "note": "上游能力和自己改造部分的边界还不够稳"
        }
      ]
    }
  }
}
```

## `feedback.md`

Recommended role:

- human-readable archive of the explicit feedback already saved into `feedback.json`
- quick scan of what was marked weak, improving, or mastered for each pack

## Local Review UI

Project-local review files:

- `review-pack.ps1`
- `.interview/review-pack.html`

Recommended flow:

1. Generate a new pack.
2. Run `./review-pack.ps1`.
3. Mark each question as `weak`, `improving`, `mastered`, or `skip`.
4. Save the feedback so it updates `feedback.json`, `feedback.md`, and `profile-memory.md`.
