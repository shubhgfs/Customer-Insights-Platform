
# 🧠 Customer Insights Platform — Technical Documentation

## Overview

The **Customer Insights Platform (CIP)** is a **multi-agentic AI system** developed for senior stakeholders such as the **CEO, CXOs, and General Managers**. Its primary purpose is to allow users to interact with business intelligence via **natural language queries**, enabling:

* Natural language to SQL transformation
* Retrieval of call transcripts relevant to specific queries
* Insightful, agent-driven collaboration between data and context

This is built using the **Agno Framework** on the backend and **Agno Playground** as the frontend interface.

---

## 💡 Core Capabilities

### Agents & Team Collaboration

CIP uses two specialized agents:

* `SQL Analyst Agent`: Converts natural language to SQL and fetches insights from a structured SQLite database.
* `Transcript Reasoning Agent`: Retrieves and reasons over customer-sales transcripts using vector search.

These agents are orchestrated in a **collaborative Agno Team** called `Customer Insight Team`, supporting shared memory, contextual reasoning, and hybrid tool-based interactions.

---

## 🛠️ Frameworks and Tooling

| Component            | Tool/Framework                                  |
| -------------------- | ----------------------------------------------- |
| Backend              | Agno Framework                                  |
| Frontend             | Agno Playground                                 |
| Embedding            | Azure OpenAI Embedder (Text Embedding 3 Large)  |
| Vector DB            | Weaviate (HNSW, Cosine Distance, Hybrid Search) |
| Storage              | SQLite via `SqliteStorage`                      |
| Programming Language | Python                                          |

---

## 🔐 Embedding Configuration

**Embedder**: `AzureOpenAIEmbedder`

* **Deployment**: `text-embedding-3-large`
* **API Version**: `2024-12-01-preview`
* ⚠️ **Important**: The model has a context limit of **8192 tokens**. Large documents exceeding this limit are skipped. You may need to explore models with extended token limits.

---

## 🗃️ Storage Design

### SQLite Storage Files

* `tmp_sql_agent.db`: For SQL query history and context
* `tmp_transcription_agent.db`: For transcript query interactions
* `tmp_cip_team.db`: For storing team-level conversation history

---

## 🔧 Agent Breakdown

### 1. SQL Analyst Agent

**Purpose**: Transform natural language queries into SQL and return human-readable interpretations.

**Key Components**:

* **Knowledge Base**: `knowledge.json` (contains query ID, user query, reasoning, SQL, and interpretation)
* **Tools**:

  * `SQLTools`: Executes SQL queries
  * `KnowledgeTools`: Loads structured SQL knowledge
  * `ThinkingTools`: Enhances reasoning over SQL outputs
  * `ReasoningTools`: Injects additional interpretability
* **Database**: Connected via `SqliteStorage` to a SQLite database with insurance sales and underwriting data

**VectorDB**:

* Backend: Weaviate
* Collection: `master`
* Search Type: Hybrid
* Distance: Cosine
* Index: HNSW

**Agent Config**:
Defined in `sql_agent_config.json` containing:

* `system_message`, `description`, `goal`, `instruction`, `expected_output`, `context`

---

### 2. Transcript Reasoning Agent

**Purpose**: Retrieve the most relevant **transcript segments** in response to a user’s query.

**Key Components**:

* **12 distinct vector indexes**, created via `TextKnowledgeBase` for transcripts
* **Metadata per document**: `brand`, `product`, `sales_status`, `year`, `month`, `day`, `content`
* **VectorDB**:

  * Collection: `transcription_master`
  * Index Type: HNSW, Distance: Cosine, Hybrid Search
* **Chunk Size**: 1000 tokens per document
* **Combined Knowledge Base**: Uses `CombinedKnowledgeBase` to aggregate all 12 indexes

⚠️ **Important**: Documents exceeding **8192 tokens** are currently skipped due to embedding model limitations. Consider model upgrade or document chunking strategy.

**Tools**:

* `TranscriptionKnowledgeTool`: Extracts relevant text chunks from vector DB
* `ThinkingTools`: Supports multi-step reasoning

**Agent Config**: `transcription_agent_config.json`, which includes:

* Role definition, instructions, and output expectations

---

## 👥 Team: Customer Insight Team

The agents work together via the **Agno Team** class under the team name: `Customer Insight Team`.

### Team Configuration

* **Members**: `SQL Analyst Agent`, `Transcript Reasoning Agent`
* **Team Modes**: `collaborate`, `coordinate`, `route`
* **Knowledge Base**: Combined vector index from both SQL and transcript knowledge bases (`Combined Master`)
* **Tools Enabled**:

  * Team knowledge search
  * Member tool interaction
  * Shared memory and state
  * Agentic context awareness

**Team Config**: Defined in `cip_team_config.json`, with:

* `description`, `instructions`, `expected_output`, `context`, `success_criteria`

---

## 🧩 System Architecture

```plaintext
                +--------------------------+
                |    CEO / CXO / GM User   |
                +------------+-------------+
                             |
                   Natural Language Query
                             |
                    +--------v---------+
                    |  Agno Playground |
                    +--------+---------+
                             |
          +------------------+-------------------+
          |                                      |
+---------v----------+              +------------v------------+
| SQL Analyst Agent  |              | Transcript Reasoning Agent |
| - knowledge.json   |              | - 12 vector indexes       |
| - SQLite DB Query  |              | - transcript metadata     |
+---------+----------+              +------------+-------------+
          \                                     /
           \            +---------------------+
            \----------->  Customer Insight Team  <----------+
                         +---------------------+            |
                                        ↑                    |
                                Team Reasoning Loop          |
                                        ↑                    |
                                Result Aggregation           |
                                        ↑                    |
                            Final Natural Language Output    |
```

---

## ✅ Success Criteria

The platform is considered successful when:

* CXOs receive context-rich, business-relevant insights from natural queries
* Transcript data is retrievable with high relevance and traceability
* SQL results are interpretable, verifiable, and actionable
* The agents collaborate meaningfully and efficiently using Agno’s orchestration

---