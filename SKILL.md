---
name: resume-interview-pack
description: Generate a high-probability interview question pack from a candidate's resume, resume-backed project code directories, interview notes, and knowledge bases. Use when Codex needs to produce interview questions, answer skeletons, expanded answers, follow-up questions, answer reviews, or a persistent interview profile for technical interviews. Trigger on requests such as generating likely interview questions, organizing project deep-dive questions, adding classic fundamentals questions, adding hot AI or agent questions, refreshing a candidate profile, or reviewing a draft interview answer.
---

# Resume Interview Pack

Generate reusable interview packs from four source types:

- resume content
- project code directories referenced by the resume
- interview notes used as style and attention signals
- local knowledge bases used to support project, principle, engineering, and fundamentals answers

Always write generated packs to `interview-packs/pack-YYYYMMDD.md`.  
Always write answer reviews to `interview-packs/review-YYYYMMDD.md`.

Do not include a self-introduction section.  
Always organize output into exactly these five sections, in order:

1. Project Deep Dive
2. Principles and Tradeoffs
3. System Design and Engineering
4. Fundamentals
5. Hot AI and Agent Topics

## Required Inputs

Use project-local candidate state under:

- `.interview/profile.json`
- `.interview/profile-memory.md`
- `.interview/feedback.json` when present
- `.interview/feedback.md` when present

If `.interview/profile.json` is missing, ask the user to fill the template described in [references/profile-schema.md](references/profile-schema.md).

If `.interview/profile-memory.md` is missing and the user asks to generate a pack, build it first from:

- the resume file
- the configured project directories
- configured interview notes
- configured knowledge bases

On later runs, prefer reusing `.interview/profile-memory.md` instead of re-reading every source.  
Only rebuild the memory file when the user explicitly asks to refresh, says the resume changed, replaces project paths, or asks to rebuild the profile.

## Source Priorities

Use sources in this order:

1. Resume project descriptions and responsibilities
2. Interview notes as style and attention signals
3. Explicit user feedback from `.interview/feedback.json` and `.interview/feedback.md`
4. Resume-backed project directories as answer evidence and grounding support
5. Knowledge bases for project, principle, engineering, and fundamentals answers
6. Persistent profile memory for historical weak spots and stable phrasing
7. Hot AI and agent topic references for general and current-practice answers

Treat interview notes as reference signals, not as a raw question bank.  
Do not copy interview-note questions verbatim unless the user explicitly asks for that.  
Instead, infer:

- what interviewers tend to care about
- how deeply they push on project details
- whether they bias toward project, principles, systems, or fundamentals
- what follow-up style is common

Treat project code directories differently from resume and interview notes:

- do not let code structure directly define the main interview question set by default
- use code primarily to strengthen answers, validate claims, and prepare plausible follow-ups
- do not introduce a major project question solely because a repository contains a module, dependency, or upstream framework reference
- only let code become a primary question source when the user explicitly asks for code-deep-dive or project-authenticity interrogation

## Reading Strategy

### Resume

Extract:

- project names
- ownership and responsibilities
- stack, metrics, and claims
- details likely to be challenged

If `projects[].resume_claim` is present in `.interview/profile.json`, treat it as a higher-priority hint for that project's intended framing. If it is absent, rely on the resume itself plus inspected project files.

Default resume format is Markdown or plain text.  
If the configured resume is not readable as text, stop and ask the user for a Markdown or TXT version.

### Project Directories

Use a bounded read strategy. Prefer:

- `README*`
- dependency and build manifests
- config files
- clear entrypoints
- top-level module layout
- a small number of likely core files

By default, use project directories for answer support, not for question invention.  
Specifically:

- use visible project evidence to make `Expanded Answer` and `Follow-Up Quick Answers` more grounded
- use visible project evidence to check whether a resume claim seems supported, weakly supported, or not yet confirmable
- use visible project evidence to prepare likely engineering follow-ups after a resume-driven main question is already selected

Do not pretend to understand a whole repository if the visible evidence is thin.  
If a resume claim cannot be grounded from the inspected project files, mark the answer as uncertain rather than inventing support.

### Interview Notes

Use interview notes only to infer likely question style:

- likely interviewer focus
- likely depth
- likely follow-up pattern
- likely framing style

### Knowledge Bases

Use knowledge bases for:

- project-adjacent principle explanations
- architecture tradeoffs
- engineering terminology
- classic fundamentals support

Do not use knowledge bases as the default source for Hot AI and Agent Topics answers.  
That category should prefer general frameworks and mainstream practice patterns.

### Persistent Profile Memory

Use `.interview/profile-memory.md` to preserve:

- project summaries
- repeated weak spots
- mastered topics and already-stable knowledge points
- historical representative questions
- preferred answer phrasing
- useful follow-up patterns
- stable notes about the user's AI workflow and framework choices
- recent pack-to-pack updates about what is still weak, improving, or already stable

### Explicit Feedback Files

Use `.interview/feedback.json` and `.interview/feedback.md` as the highest-confidence signal for what the user currently marks as:

- weak
- improving
- mastered

Prefer explicit feedback over heuristic inference when the two conflict.

## Output Construction

Generate about 10 questions by default with this target distribution:

- Project Deep Dive: 3
- Principles and Tradeoffs: 1
- System Design and Engineering: 1
- Fundamentals: 2
- Hot AI and Agent Topics: 3

If the available material is too sparse, keep the same section structure but reduce question count rather than fabricating details.

For question generation, separate source roles clearly:

- `Question` should be driven mainly by the resume, the resume-visible project framing, and the inferred interviewer style from interview notes
- `Expanded Answer` and `Follow-Up Quick Answers` may use project code, knowledge bases, and stable profile memory to make the answer concrete
- do not let repository-only details silently become the main question unless the user explicitly asks for a code-driven deep dive

Every question card must use this order:

1. Question
2. What It Tests
3. One-Minute Skeleton
4. Expanded Answer
5. Possible Follow-Ups
6. Follow-Up Quick Answers
7. Why This Is Likely

Use spoken interview language, not essay style.  
The expanded answer should sound like something the candidate could actually say.  
The follow-up quick answers should be compact spoken answers, not one-line fragments and not mini-essays. Treat each follow-up answer independently: it should read like a small spoken paragraph that can stand on its own, but still be compact enough to be spoken in under about two minutes.  
If a claim is not well-supported by the configured sources, say so plainly.

Use the exact Markdown structure from [references/question-template.md](references/question-template.md).  
Use the section order from [references/scenario-layout.md](references/scenario-layout.md).  
Use the answer style guardrails from [references/answer-rubric.md](references/answer-rubric.md).

## Mode: Generate Pack

When the user asks to generate a question pack:

1. Load `.interview/profile.json`.
2. Load `.interview/profile-memory.md` if it exists and is still valid.
3. If memory is missing or explicitly stale, rebuild it before generating the pack.
4. Load `.interview/feedback.json` and `.interview/feedback.md` when they exist.
5. Gather source signals from resume, project directories, interview notes, knowledge bases, and explicit feedback.
6. Use explicit feedback to bias question selection:
   - revisit weak topics more often
   - keep improving topics warm
   - reduce over-repetition of already-mastered topics unless they are core resume risk points
7. Generate the five required sections with this split:
   - main questions come from resume framing plus interview-note style signals
   - project directories support answers, grounding, and follow-up realism
8. Add `Source Summary` only when the user explicitly asks for provenance, when the configured source set changed materially, or when the pack would otherwise be hard to interpret.
9. Add a short `Interview Notes Influence` section explaining how the notes shaped the pack without copying original questions.
10. Write the final output to `interview-packs/pack-YYYYMMDD.md`.
11. After writing the pack, update `.interview/profile-memory.md` based on the new pack.
12. If the user wants interactive review outside the chat, point them to `review-pack.ps1`, which serves `.interview/review-pack.html` and writes feedback back into the project files.

When updating `.interview/profile-memory.md` after a pack:

- prefer explicit feedback from `.interview/feedback.json` over guessed weak/mastered inference
- add or refine repeated weak spots exposed by the pack
- add or refine mastered topics that are already stable enough to reuse in later packs
- add a dated recent-update entry summarizing what became weaker, what became stronger, and what still needs practice
- keep stable facts concise instead of appending duplicate notes forever

Use these promotion rules for mastered topics:

- mark a topic as mastered when it is repeatedly supported by grounded project evidence, stable answer structure, or explicit user confirmation
- if evidence is mixed, keep the topic under weak spots or note it as improving rather than mastered
- do not promote a topic to mastered only because the model generated a plausible answer once

## Mode: Refresh Profile

When the user asks to refresh the interview profile:

1. Re-read all configured sources.
2. Re-read `.interview/feedback.json` and `.interview/feedback.md` if they exist.
3. Rebuild `.interview/profile-memory.md`.
4. Preserve stable facts that remain true.
5. Replace stale summaries and weak spots with the newly grounded view.
6. Rebuild mastered topics and recent pack updates conservatively, keeping only grounded or user-confirmed items.
7. Do not generate a question pack unless the user also asks for one.

Use the structure from [references/profile-schema.md](references/profile-schema.md) when rebuilding memory.

## Mode: Review Answer

When the user provides a draft answer:

1. Determine which section the question belongs to.
2. Score the answer against:
   - correctness
   - depth
   - specificity
   - consistency with configured resume and projects
   - spoken interview quality
3. Produce:
   - brief verdict
   - strengths
   - gaps
   - better one-minute skeleton
   - better expanded answer
   - likely follow-up
4. Write the output to `interview-packs/review-YYYYMMDD.md`.
5. If the review clearly shows a stable strength or a repeated weakness, update `.interview/profile-memory.md` accordingly.

## Local Review Flow

This skill supports an out-of-chat feedback loop:

1. Generate a pack.
2. Run `./review-pack.ps1` from the workspace root.
3. Review the latest pack in the local browser page served from `.interview/review-pack.html`.
4. Save the feedback.
5. Let future pack generation and profile refresh read `.interview/feedback.json` and `.interview/feedback.md`.

The local review flow should update:

- `.interview/feedback.json`
- `.interview/feedback.md`
- `.interview/profile-memory.md`

## Fundamentals Questions

Use [references/fundamentals-topics.md](references/fundamentals-topics.md) to choose classic interview questions.

Prefer fundamentals that fit the user's stack or claims.  
Examples include:

- caching
- Redis
- MySQL
- indexes
- transactions
- message queues
- concurrency
- thread pools
- JWT and auth
- RPC and service boundaries

Do not turn this into a generic random FAQ dump.  
Tie the question choice back to the candidate's projects whenever possible.
When using project evidence here, use it to sharpen the answer and likely follow-ups, not to override a resume-driven main question choice.

## Hot AI and Agent Topics

Use [references/hot-topics.md](references/hot-topics.md) for Hot AI and Agent Topics.

This category must include general and current-practice questions such as:

- how the user uses AI day to day
- how the user does AI coding
- how the user validates AI output
- how to choose between LangChain, LangGraph, raw SDK approaches, or MCP-style integration
- why the user chose their current AI framework
- how to reason about agent tooling, memory, safety, permissions, and orchestration

Before selecting the 3 hot-topic questions, inspect the most recent pack under `interview-packs/`.

- Do not reuse the same 3 hot-topic buckets in consecutive packs.
- Prefer buckets that were not used in the latest pack.
- Only repeat a bucket from the latest pack when the user explicitly asks for it, or when feedback marks it as a weak area worth reinforcing.
- Keep section 5 varied across adjacent packs instead of defaulting to the same trio every time.

For Hermes, OpenClaw, CC source, and similar open-source projects:

- only generate shallow familiarity questions
- do not generate source-level interrogation
- focus on what the project is, what route it represents, and why it is worth following

When local notes already contain material about those projects, use them to polish phrasing.  
When they do not, fall back to a generic analysis frame:

- what the project is
- what engineering route it seems to represent
- why it is interesting
- a one-sentence takeaway
