# Hot AI and Agent Topics

Use this file for the fifth section of the interview pack.

## Required Hot Topic Buckets

Always prefer a mix from these buckets:

- Daily AI usage
- AI coding workflow
- Framework selection
- Agent architecture
- RAG vs agent boundaries
- MCP and tool integration
- Safety, permissions, and validation
- Open-source project awareness

## Rotation Rule

When generating the 3 hot-topic questions for a new pack:

- inspect the most recent pack in `interview-packs/` first
- do not reuse the same 3 buckets in consecutive packs
- prefer buckets that were not used in the most recent pack
- only repeat a bucket from the latest pack when:
  - the user explicitly asks for that topic
  - recent feedback marks it as `weak`
  - the remaining materials are too thin to support a better rotation

Default policy:

- rotate across the unused buckets before returning to a repeated trio
- if the latest pack used `AI coding workflow`, `Framework selection`, and `Open-source project awareness`, the next pack should prefer buckets like `Daily AI usage`, `Agent architecture`, `RAG vs agent boundaries`, `MCP and tool integration`, or `Safety, permissions, and validation`
- avoid turning the fifth section into a fixed FAQ block; keep the category stable, but rotate the exact angles

## Daily AI Usage

Good prompts:

- How do you use AI in day-to-day development?
- What parts of your workflow benefit most from AI?
- Where do you intentionally avoid using AI?

Good answer frame:

- where AI helps
- where manual verification is still required
- what the candidate does to reduce hallucinations or shallow output

## AI Coding Workflow

Good prompts:

- How do you do AI coding in practice?
- How do you prevent AI from making unsafe or low-quality code changes?
- How do you validate AI-generated code?

Good answer frame:

- use AI for exploration, boilerplate, review, or refactoring
- keep ownership of architecture and correctness
- validate with tests, diff review, and source inspection

## Framework Selection

Good prompts:

- How do you choose between LangChain, LangGraph, a raw model SDK, and MCP-style integration?
- Why did you choose your current AI framework?
- In what cases would you move away from your current framework?

Default answer frame:

- scenario
- candidate options
- decision criteria
- current choice
- drawbacks
- switch conditions

## Agent Architecture

Good prompts:

- What are the key parts of an agent system?
- How do you think about tools, memory, planning, and guardrails?
- Where is the boundary between workflow and agent?

## RAG and MCP

Good prompts:

- What is the boundary between RAG and agent systems?
- What problem does MCP solve?
- When would you use MCP rather than hard-wired tool integration?

## Safety and Validation

Good prompts:

- What are the main risks in AI coding?
- How do you constrain model behavior in production?
- How do you think about sandbox, human approval, and verification loops?

## Open-Source Project Awareness

Only generate shallow familiarity questions for projects like Hermes, OpenClaw, and CC source.

Allowed question styles:

- Have you looked at any recent open-source agent projects?
- Do you know what Hermes or OpenClaw roughly represent?
- If you had to summarize CC source in one sentence, how would you say it?

Do not generate source-level deep dives.

Use this lightweight answer frame:

- what the project is
- what engineering route it seems to represent
- why it is worth following
- one-sentence takeaway
