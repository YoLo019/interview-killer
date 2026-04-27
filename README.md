<div align="center">

# interview-killer

> Resume-backed interview pack skill for Codex

[![Skill](https://img.shields.io/badge/skill-resume--interview--pack-0f766e)]()
[![Runtime](https://img.shields.io/badge/runtime-python%203-3776AB)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()

</div>

`interview-killer` is a Codex skill package built for technical interview prep.

It does not generate generic question banks. It reads your resume, the codebases behind your resume projects, your interview notes, and your own knowledge bases, then produces a structured interview pack with likely questions, spoken answer skeletons, expanded answers, and follow-up answers.

It also keeps a persistent candidate memory and supports an interactive review flow, so each new pack can gradually adapt to your weak spots and already-mastered topics.

## What It Does

- Generates a high-probability interview pack from four inputs:
  - resume
  - resume-backed project directories
  - interview notes as interviewer-style signals
  - knowledge bases as answer support
- Organizes output into five fixed sections:
  - Project Deep Dive
  - Principles and Tradeoffs
  - System Design and Engineering
  - Fundamentals
  - Hot AI and Agent Topics
- Writes packs to local Markdown files for later review
- Maintains a persistent interview profile under `.interview/`
- Supports explicit feedback with `weak`, `improving`, and `mastered`
- Includes a local browser review UI for pack-by-pack feedback

## Use Cases

Use this skill when you want to:

- generate likely interview questions from your own resume and projects
- prepare project deep-dive questions instead of generic template questions
- add classic backend fundamentals that match your stack
- add hot AI and agent questions without repeating the same trio every time
- review your answer quality and update long-term weak spots

## How It Works

The skill reads project-local state from:

```text
.interview/profile.json
.interview/profile-memory.md
.interview/feedback.json
.interview/feedback.md
```

It uses sources in this general order:

1. Resume and project responsibilities
2. Resume-backed project repositories
3. Interview notes as style and follow-up signals
4. Explicit feedback
5. Knowledge bases
6. Persistent profile memory
7. Built-in hot-topic references

Generated packs are written to:

```text
interview-packs/pack-YYYYMMDD.md
```

Answer reviews are written to:

```text
interview-packs/review-YYYYMMDD.md
```

## Quick Start

### 1. Put the skill in your Codex workspace or skill directory

For a project-local setup:

```text
.agents/skills/resume-interview-pack/
```

For a user-level setup, copy it into your Codex skills directory.

### 2. Create your interview profile

Create:

```text
.interview/profile.json
```

Minimal example:

```json
{
  "resume_path": "C:\\Users\\YourName\\resume.md",
  "projects": [
    {
      "name": "HappyFlow",
      "path": "D:\\projects\\happyflow"
    }
  ],
  "materials": {
    "interview_notes": [
      "C:\\Users\\YourName\\notes\\interview-notes.md"
    ],
    "knowledge_bases": [
      "C:\\Users\\YourName\\notes\\rag-kb.md"
    ]
  }
}
```

### 3. Ask Codex to generate a pack

Examples:

```text
根据我的简历和项目生成高概率面试题
```

```text
帮我整理项目深挖题和标准回答
```

```text
帮我补一些常问八股和热门 AI / Agent 题
```

### 4. Review and feed back

This repo also includes a local review tool:

- `scripts/review_server.py`

In the original workspace version, it is commonly paired with a launcher such as:

```text
review-pack.ps1
review-pack.cmd
启动题包反馈.cmd
```

The review UI lets you:

- choose a generated pack
- mark each question as `weak`, `improving`, or `mastered`
- write a short note
- save feedback back into `.interview/feedback.json`, `.interview/feedback.md`, and `.interview/profile-memory.md`

## Output Shape

Each generated question card follows a fixed structure:

1. Question
2. What It Tests
3. One-Minute Skeleton
4. Expanded Answer
5. Possible Follow-Ups
6. Follow-Up Quick Answers
7. Why This Is Likely

The answers are written in spoken interview language rather than article style.

## Hot AI / Agent Topics

The fifth section is not just project-adjacent AI talk.

It can include topics such as:

- daily AI usage
- AI coding workflow
- framework selection
- agent architecture
- RAG vs agent boundaries
- MCP and tool integration
- safety, permissions, and validation
- shallow open-source awareness for Hermes, OpenClaw, and CC-like projects

The skill also avoids reusing the exact same hot-topic trio in consecutive packs unless:

- you explicitly ask for it
- feedback marks it as weak

## Repository Structure

```text
interview-killer/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── answer-rubric.md
│   ├── fundamentals-topics.md
│   ├── hot-topics.md
│   ├── profile-schema.md
│   ├── question-template.md
│   └── scenario-layout.md
├── scripts/
│   └── review_server.py
├── README.md
├── .gitignore
└── LICENSE
```

## Notes

- This repo contains the skill package itself, not your private resume or generated packs.
- Do not commit your own `.interview/` data or `interview-packs/` outputs into the public repo.
- If your resume is not plain text or Markdown, convert it before using the skill.

## License

MIT. See [LICENSE](./LICENSE).
