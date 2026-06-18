# 🧠 Synapse

> Transform natural language into a persistent knowledge graph.

Synapse is a Python library that converts unstructured text into a structured knowledge graph by extracting concepts and relationships from natural language.

Instead of storing information as raw text, Synapse organizes information into a graph structure that can be queried, traversed, and extended for building intelligent systems and memory systems.

---

## ✨ Features

- Natural language → structured relationships
- Persistent graph storage
- Duplicate prevention
- Case-insensitive querying
- Multi-hop relationship traversal
- Local-first architecture
- Provider-agnostic design
- Extensible memory engine

---

## 📦 Installation

```bash
pip install synapse-ai
```

---

## ⚡ Quick Start

```python
from synapse import Synapse

brain = Synapse()

brain.add(
    "CEO of Apple met Microsoft executives in Seattle."
)

brain.save()

print(
    brain.get_relations("Apple")
)

print(
    brain.get_indirect_relations("CEO of Apple")
)
```

---

## Example

### Input

```text
Python is used for AI and TensorFlow is used in AI.
```

### Extracted Graph

```python
{
    "python": [
        ("used_for", "ai")
    ],
    "tensorflow": [
        ("used_in", "ai")
    ]
}
```

---

## Project Structure

```text
synapse/
├── __init__.py
├── synapse.py
├── graph.py
├── query.py
├── processor.py
├── extractor.py
├── persistence.py
└── utils.py
```

---

## ⚙️ Design Principles

- Simplicity over complexity
- Local-first architecture
- Incremental development
- Extensibility
- No overengineering

---

## 📌 Current Status

### ✅ V1 Complete

Implemented features:

- Text ingestion
- Relationship extraction
- Graph construction
- Graph persistence
- Query system
- Multi-hop traversal
- Python package support
- Provider-agnostic extractor architecture

---

# 🗺️ Roadmap

## V2 — Conversational Memory Layer

Build a conversational interface on top of the graph.

Planned capabilities:

- Memory-backed conversations
- Graph-aware retrieval
- Contextual question answering
- Better reasoning over stored knowledge
- Persistent long-term memory

---

## V3 — Agentic Knowledge Graph

Integrate coding agents and sandboxed environments.

Planned capabilities:

- Claude Code integration
- Codex integration
- Live graph construction during conversations
- Automatic graph updates
- Multi-session memory
- Knowledge graph visualization

---

## V4 — Portable Intelligence

Turn Synapse into a transferable memory engine.

Planned capabilities:

- Import knowledge graphs
- Export knowledge graphs
- Transfer memory between LLMs
- Local execution
- Offline mode
- Personal AI memory system

Example:

```text
Claude
    ↓
Knowledge Graph
    ↓
Export
    ↓
GPT
    ↓
Continue with the same memory
```

---

## 🚀 Vision

Modern AI systems own the intelligence, but they also own the memory.

Synapse aims to separate the two.

The long-term goal is to make memory portable, persistent, and independent of any single model provider.

Memory should belong to the user, not the model.

---

## 🧑‍💻 Author

### Piyush Garg

AI/ML enthusiast interested in:

- Knowledge Graphs
- LLM Systems
- Intelligent Agents
- Machine Learning Infrastructure

Building systems at the intersection of memory and intelligence.

---

## 📄 License

MIT License