import git
from .persistence import load_compressed_context, save_compressed_context, load_metadata, save_metadata
from .git_manager import (
    get_repository_changes,
    split_commit_by_file
)
from ollama import chat
import json

repo = git.Repo(search_parent_directories=True)


MAX_PROMPT_SIZE = 30000
MAX_FILES_PER_COMMIT = 3

VALID_KEYS = {
    "repository_purpose",
    "architecture",
    "evolution",
    "decisions",
    "features",
    "design_principles",
    "current_capabilities",
}



INITIAL_PROMPT_TEMPLATE = """
You are Synapse Repository Memory Builder.

TASK

Construct the initial compressed repository memory from a single repository change unit.

This prompt is executed only once when no compressed_context.json exists.

INPUT

You will receive:

per_commit_diff

per_commit_diff contains:

* Commit message
* Commit diff
* Repository changes represented by that commit

Treat per_commit_diff as the only source of truth.

GOAL

Extract durable repository knowledge while maximizing compression.

The produced memory should capture only information likely to remain useful after many future commits.

Focus on:

* Repository purpose
* Architecture
* Components
* Relationships
* Capabilities
* Design decisions
* Design principles
* Evolution signals

KNOWLEDGE RETENTION PRIORITY

1. Architecture
2. Major decisions
3. Component relationships
4. Capabilities
5. Evolution
6. Design principles
7. Features
8. Implementation details

ARCHITECTURE EXTRACTION

Capture:

* Components
* Subsystems
* Services
* Layers
* Data flow relationships
* Dependencies

Examples:

* Query Engine depends_on Graph Store
* Extractor feeds Knowledge Graph
* Persistence Layer stores Repository Memory

DECISION EXTRACTION

Capture durable problem → solution relationships.

Examples:

Problem:
Duplicate processing

Solution:
Commit checkpointing

Problem:
Repository scale

Solution:
Incremental compression

EVOLUTION EXTRACTION

Capture meaningful architectural progression.

Examples:

* Full history processing evolved_into incremental processing
* Flat storage evolved_into structured memory

Only preserve evolution that explains architecture or capabilities.

CAPABILITY EXTRACTION

Capture what the repository can accomplish.

Examples:

* Repository understanding
* Incremental updates
* Memory compression
* Knowledge extraction

DESIGN PRINCIPLE EXTRACTION

Capture recurring engineering philosophy.

Examples:

* Incremental processing
* Provider independence
* Local-first execution
* Token efficiency

IGNORE

Do not store:

* Formatting changes
* Whitespace changes
* Comment-only changes
* Temporary experiments
* Commit-level summaries
* File-level summaries
* Exact variable names
* Exact function names
* Exact implementation details

COMPRESSION RULES

* Preserve maximum semantic meaning.
* Minimize token count.
* Merge equivalent concepts.
* Prefer abstractions over implementation details.
* Prefer architecture over code.
* Prefer capability over implementation.
* Avoid redundancy.
* Avoid restating commit contents.

HALLUCINATION RULES

* Only use information supported by per_commit_diff.
* Do not invent architecture.
* Do not invent capabilities.
* Do not infer unsupported future plans.

OUTPUT FORMAT

{{
"repository_purpose": [],
"architecture": [],
"evolution": [],
"decisions": [],
"features": [],
"design_principles": [],
"current_capabilities": []
}}

IMPORTANT

The output becomes compressed_context.json.

Return only valid JSON.

Return only the JSON object shown above.

No markdown.

No explanations.

No text outside JSON.

per_commit_diff:

{initial_commit_diff}

"""


UPDATE_PROMPT_TEMPLATE = """
You are Synapse Repository Memory Maintainer.

TASK

Maintain the repository's canonical Repository Memory.

You will receive:

1. current_compressed_context
2. per_commit_diff

current_compressed_context is the repository's existing memory.

per_commit_diff contains one new repository change consisting of:

- Commit message
- Commit diff

Treat both inputs as authoritative.

--------------------------------------------------
PRIMARY OBJECTIVE
--------------------------------------------------

Produce a NEW Repository Memory that completely replaces the previous one.

The Repository Memory must become MORE consistent after every update.

It should converge toward a stable repository ontology instead of continually growing.

--------------------------------------------------
UPDATE PROCESS
--------------------------------------------------

1. Interpret current_compressed_context as the existing repository ontology.

2. Extract only durable knowledge from per_commit_diff.

3. Merge the new knowledge into the ontology.

4. Rewrite older concepts whenever a cleaner or more general representation exists.

5. Return the updated Repository Memory.

--------------------------------------------------
STABILITY RULE
--------------------------------------------------

Most commits should modify only a small portion of the Repository Memory.

Do not rewrite unrelated concepts.

Only update sections affected by the current repository change.

Large rewrites should occur only when the repository architecture has genuinely changed.

--------------------------------------------------
ONTOLOGY INVARIANTS
--------------------------------------------------

The following rules must ALWAYS hold.

1. Every concept appears exactly once across the entire Repository Memory.

2. Every concept belongs to exactly ONE category.

3. Never duplicate concepts using different wording.

4. Prefer one canonical representation.

5. Prefer shorter wording when meaning is preserved.

6. Prefer abstraction over implementation details.

7. The Repository Memory should stabilize over time.

--------------------------------------------------
FIELD DEFINITIONS
--------------------------------------------------

repository_purpose

What fundamental problem does this repository solve?

Maximum: 2 items.

--------------------------------------------------

architecture

Describe WHAT components exist.

Examples:

- Knowledge graph
- Persistence layer
- LLM extractor
- Query engine

Do NOT include:

- Capabilities
- Features
- Function names
- Method names
- Utilities

--------------------------------------------------

current_capabilities

Describe WHAT the repository can currently do.

Do NOT describe HOW.

Examples:

- Extract knowledge from text
- Query relationships
- Persist graph
- Traverse relationships

--------------------------------------------------

features

Describe user-visible functionality.

If something already exists under current_capabilities, do not repeat it.

--------------------------------------------------

design_principles

Store engineering philosophy only.

Examples:

- Local-first
- Provider agnostic
- Simplicity
- Incremental development

--------------------------------------------------

decisions

Store durable engineering choices.

Examples:

- JSON persistence
- Adjacency-list graph
- Provider abstraction
- Execution guards

Do NOT require explicit problem → solution wording.

--------------------------------------------------



--------------------------------------------------
evolution
--------------------------------------------------

Store only major historical transitions that actually occurred in the repository.

A transition should describe how the repository fundamentally changed over time.

Examples:

- Graph-only processing → LLM-assisted extraction
- In-memory storage → Persistent JSON storage
- Gemini-specific extractor → Provider abstraction
- One-shot processing → Incremental processing

Evolution should describe:

- Architectural transitions
- Processing strategy changes
- Storage changes
- Major subsystem introductions
- Major subsystem replacements

Do NOT store:

- Roadmaps
- Planned versions
- Future features
- Version numbers
- Release names
- Commit history
- Minor feature additions

If the current commit does not introduce or modify a major architectural transition, leave evolution unchanged.

If no meaningful historical transitions exist, return an empty list.

--------------------------------------------------
MERGING RULES
--------------------------------------------------

If a concept already exists:

- Reuse it.
- Improve it if necessary.
- Never duplicate it.

If two concepts describe the same idea:

Merge them into one canonical concept.

Examples:

Relationship querying
Relationship retrieval

↓

Relationship querying

----------------------------------------

Persistent graph storage
JSON persistence
evolution
↓

Persistent graph storage

----------------------------------------

Indirect relationship traversal
Multi-hop traversal

↓

Multi-hop relationship traversal

--------------------------------------------------
MEMORY BUDGET
--------------------------------------------------

Repository Memory is bounded.

Adding new concepts may require:

- Merging
- Rewriting
- Removing redundant concepts

The Repository Memory must not continually grow simply because more commits are processed.

--------------------------------------------------
REMOVE
--------------------------------------------------

Never store:

- Function names
- Method names
- Variable names
- Utility functions
- Validation logic
- Exception handling
- Type hints
- Docstrings
- README examples
- Installation instructions
- Package publishing
- Testing code
- Temporary implementation details
- Commit summaries

--------------------------------------------------
KNOWLEDGE RETENTION PRIORITY
--------------------------------------------------

1. Architecture
2. Decisions
3. Component relationships
4. Capabilities
5. Evolution
6. Design principles
7. Features

--------------------------------------------------
HALLUCINATION RULES
--------------------------------------------------

Only use information supported by the inputs.

Do not invent:

- Architecture
- Components
- Capabilities
- Decisions
- Evolution

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

{{
  "repository_purpose": [],
  "architecture": [],
  "evolution": [],
  "decisions": [],
  "features": [],
  "design_principles": [],
  "current_capabilities": []
}}

Return ONLY valid JSON.

Return ONLY the JSON object.

No markdown.

No explanations.

current_compressed_context:

{current_compressed_context}

per_commit_diff:

{per_commit_diff}
"""


def generate_initial_prompt(initial_commit_diff):
    return INITIAL_PROMPT_TEMPLATE.format(
        initial_commit_diff=json.dumps(
            initial_commit_diff,
            indent=2
        )
    )


def generate_update_prompt(current_compressed_context, per_commit_diff):
    return UPDATE_PROMPT_TEMPLATE.format(
        current_compressed_context=json.dumps(
            current_compressed_context,
            indent=2
        ),
        per_commit_diff=json.dumps(
            per_commit_diff,
            indent=2
        )
    )


def clean_json_response(raw: str) -> dict:
    text = raw.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        inner_lines = []

        for line in lines[1:]:
            if line.strip() == "```":
                break
            inner_lines.append(line)

        text = "\n".join(inner_lines).strip()

    try:
        parsed = json.loads(text)

    except json.JSONDecodeError as e:
        print("=" * 80)
        print("[context_builder] JSON parse failed")
        print(e)
        print("RAW TEXT:")
        print(text)
        print("=" * 80)
        return None

    if isinstance(parsed, str):
        try:
            parsed = json.loads(parsed)
        except json.JSONDecodeError:
            return None

    if not isinstance(parsed, dict):
        print(f"[context_builder] Unexpected type: {type(parsed)}")
        return None

    validated = {
        k: parsed.get(k, [])
        for k in VALID_KEYS
    }

    for key in validated:
        if not isinstance(validated[key], list):
            validated[key] = []

    return validated


def get_response(prompt, num_predict=4096):

    try:
        response = chat(
            model="qwen3:14b-q4_K_M",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            think=False,
            options={
                "num_predict": num_predict,
                "temperature": 0
            }
        )
    except Exception as e:
        print("Failed to connect to Ollama.")
        print("Make sure Ollama is running and the required model is installed.")

    raw = response["message"]["content"]

    if not raw or not raw.strip():
        print("[context_builder] Empty response from model.")
        return None

    return clean_json_response(raw)


def build_compressed_context():

    compressed_context = load_compressed_context()
    metadata = load_metadata()
    repo_changes = get_repository_changes(metadata)

    if not repo_changes:
        return

    start = 0

    # Initial memory construction
    if compressed_context == {}:

        initial_prompt = generate_initial_prompt(
            repo_changes[0]
        )

        compressed_context = get_response(
            initial_prompt
        )

        if compressed_context is None:
            print(
                "[context_builder] Initial memory generation failed."
            )
            return

        save_compressed_context(compressed_context)
        start = 1

    success = True

    for change in repo_changes[start:]:

        update_prompt = generate_update_prompt(
            compressed_context,
            change
        )

        prompt_too_large = (
            len(update_prompt) > MAX_PROMPT_SIZE
        )

        too_many_files = (
            change["diff"].count("diff --git")
            > MAX_FILES_PER_COMMIT
        )

        if prompt_too_large or too_many_files:
            changes_to_process = split_commit_by_file(change)
        else:
            changes_to_process = [change]

        for current_change in changes_to_process:

            update_prompt = generate_update_prompt(
                compressed_context,
                current_change
            )

            result = get_response(update_prompt, num_predict=4096)

            if result is None:
                print(
                    f"[context_builder] Failed on "
                    f"{current_change['sha'][:8]}"
                )
                success = False
                break

            compressed_context = result
            save_compressed_context(
                compressed_context
            )

        if not success:
            break

    if success:
        metadata["last_processed_commit"] = (
            repo.head.commit.hexsha
        )
        save_metadata(metadata)