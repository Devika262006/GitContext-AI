# 🧠 GitContext-AI

### End-to-End Codebase Intelligence & Developer Copilot using Hybrid RAG

GitContext-AI is an intelligent codebase assistant that understands software repositories and provides accurate, context-aware answers to developer questions.

It combines **AST-based code understanding, semantic search, BM25 keyword search, hybrid retrieval, reranking, and Gemini-powered RAG** to retrieve relevant code and generate grounded answers.

---

## 🚀 Key Features

- 🔗 GitHub repository ingestion
- 📂 Intelligent source-code discovery
- 🌳 AST-based Python code parsing
- ✂️ Structure-aware code chunking
- 🧠 Semantic embeddings using FastEmbed
- 🔎 Vector search using Qdrant
- 🔤 BM25 keyword search
- 🔀 Hybrid semantic + keyword retrieval
- 🎯 Cross-encoder reranking
- 🤖 Gemini-powered RAG answer generation
- 📌 Dynamic source-code citations
- 👀 Expandable "View Code" source snippets
- 📊 Query performance metrics
- 📈 Retrieval quality evaluation
- 🧪 Automated test suite
- ⚡ FastAPI backend
- 💻 Interactive developer dashboard
- 🔐 Environment-variable based secret management

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   GitHub Repository  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Repository Ingestion │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ File Discovery       │
                 │ & Filtering          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ AST Code Parser      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Code Chunking        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ FastEmbed            │
                 │ BGE-small-en-v1.5    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Qdrant Vector Store  │
                 └──────────┬───────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
        ┌────────────────┐    ┌────────────────┐
        │ Vector Search  │    │ BM25 Search    │
        └───────┬────────┘    └───────┬────────┘
                │                     │
                └──────────┬──────────┘
                           ▼
                 ┌──────────────────────┐
                 │ Hybrid Retrieval     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Cross Encoder        │
                 │ Reranking            │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Gemini RAG Generator │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ FastAPI Backend      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Web Developer UI     │
                 └──────────────────────┘