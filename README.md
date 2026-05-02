# 🧠 Synapse — Personal Knowledge Graph (PKG)

## 🚀 Overview

Synapse is a system that converts unstructured text into a structured knowledge graph.

Instead of storing information as raw text (which is hard to query and reason about), Synapse extracts **concepts** and **relationships between them**, and represents them as a graph-like dictionary.

This allows information to be:
- Structured  
- Queryable  
- Extendable for reasoning systems  

---

## 🎯 V1 — Core System (Current Focus)

**Goal:** Build a minimal, local-first knowledge graph system from text.

### What it does:
- Takes **text input**
- Extracts:
  - Concepts  
  - Relationships between concepts  
- Stores them in a **graph structure (dictionary)**  

### Example

**Input:**

Python is a programming language


**Output (conceptually):**

Python → is → programming language


---

## 🧠 Why this matters

Raw text is:
- Unstructured  
- Hard to query  
- Difficult to reason over  

A knowledge graph enables:
- Clear relationships  
- Better retrieval  
- Foundation for intelligent systems  

---

## 🏗️ Project Structure (V1)

```
synapse/
├── graph.py # Graph creation + relationship handling
├── main.py # Entry point for testing
└── README.md # Project documentation
```
---

## 🔮 Future Roadmap

### V2 — Smarter Ingestion
- Add **PDF + document ingestion**
- Improve extraction quality  
- Better graph reasoning  

### V3 — Chat Interface (RAG System)
- Build a **chat system on top of the graph**
- Combine:
  - Knowledge graph  
  - LLM reasoning  
- Enable contextual Q&A  

### V4 — Local Intelligence
- Run **local LLMs**
- Enable:
  - Offline usage  
  - Export / import knowledge graphs  
- Turn Synapse into a personal AI memory system  

---

## ⚙️ Design Principles

- Simplicity over complexity  
- Local-first system  
- Incremental development  
- No overengineering  

---

## 📌 Status

🚧 Currently building V1 — core graph system  

---

## 🧑‍💻 Author

**Piyush Garg**

AI/ML enthusiast building systems at the intersection of:
- Machine Learning  
- Knowledge Graphs  
- Intelligent Systems  

Focused on building scalable, real-world projects.