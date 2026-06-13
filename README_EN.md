
---

# UNSW Course Selection Agent

> An AI-powered course selection assistant for UNSW students based on RAG (Retrieval-Augmented Generation), FastAPI and LLM-powered Query Parsing.

---

## Project Overview

UNSW Course Selection Agent is an intelligent course planning assistant designed for UNSW postgraduate students.

The system can:

* Upload and process UNSW Handbook PDFs
* Extract course and program information
* Build a vector database for semantic retrieval
* Answer course selection questions using RAG
* Automatically understand user intent through Query Parsing
* Route different question types to appropriate retrieval strategies

The project aims to evolve from a traditional RAG chatbot into a real course planning agent.

---

## Features

### Handbook Management

* Upload Program Handbook PDFs
* Upload Course Handbook PDFs
* Automatic PDF text extraction
* File deduplication using MD5 hash

---

### Metadata Extraction

Automatically extracts metadata such as:

```json
{
    "university": "UNSW",
    "degree_level": "postgraduate",
    "year": "2026",
    "handbook_type": "course",
    "program": "Artificial Intelligence",
    "course_code": "COMP9417",
    "prerequisites": "COMP9101,COMP9801"
}
```

---

### RAG Pipeline

```text
PDF
 ↓
Chunking
 ↓
Embedding
 ↓
Chroma Vector Store
 ↓
Retriever
 ↓
Prompt Construction
 ↓
Qwen LLM
 ↓
Answer
```

---

### Query Parser Layer

The system includes a dedicated Query Parser.

Instead of directly sending user questions to the LLM, the system first converts natural language into structured instructions.

Example:

User Query:

```text
I have completed COMP9101.
Can I take COMP9417?
```

Parsed Result:

```json
{
    "question_type": "prerequisite_check",
    "target_course": "COMP9417",
    "completed_courses": [
        "COMP9101"
    ]
}
```

---

### Question Classification

Supported question types:

| Type                | Description            |
| ------------------- | ---------------------- |
| prerequisite        | prerequisite questions |
| prerequisite_check  | eligibility checking   |
| course_information  | course information     |
| program_requirement | program requirements   |
| study_planning      | study planning         |
| general             | general questions      |

---

### Agent Routing

The system automatically selects retrieval strategies based on parsed intent.

Example:

```text
Program Requirement
    ↓
Program Handbook Retrieval

Course Information
    ↓
Course Handbook Retrieval

Prerequisite Question
    ↓
Course Metadata + Handbook Retrieval
```

---

### Streaming Chat

Supports real-time response streaming through FastAPI.

```text
/chat
/chat/stream
```

---

### Conversation History

Session-based conversation memory.

Each user session maintains independent history.

---

## System Architecture

```text
User
 │
 ▼
FastAPI
 │
 ▼
Chat API
 │
 ▼
Query Parser Layer
 ├── LLM Query Parser
 └── Rule Parser (Fallback)
 │
 ▼
Structured Query JSON
 │
 ▼
RAG Service
 ├── Metadata Filter
 ├── Vector Retrieval
 ├── Session History
 └── Prompt Builder
 │
 ▼
Qwen LLM
 │
 ▼
Answer
```

---

## API Endpoints

### Upload Handbook

```http
POST /upload
```

---

### Create Session

```http
POST /session/create
```

---

### Chat

```http
POST /chat
```

---

### Streaming Chat

```http
POST /chat/stream
```

---

### Get Chat History

```http
GET /chat/history/{session_id}
```

---

## Tech Stack

### Backend

* FastAPI

### LLM

* Qwen-Max
* Tongyi Chat Model

### Embedding

* DashScope Embedding

### Vector Database

* ChromaDB

### Framework

* LangChain

### Storage

* Local File Storage
* Chroma Vector Store

---

## Current Status

### Completed

* PDF Upload
* PDF Parsing
* Metadata Extraction
* Chroma Vector Database
* RAG Question Answering
* Session Management
* Chat History
* Streaming Chat
* Query Parser
* LLM Query Parser
* Agent Routing

### Planned

* User Authentication
* User Isolation
* Study Planning Agent
* Course Dependency Graph
* Program Requirement Reasoning
* Frontend Application
* Cloud Deployment

---

## Author

UNSW Master of Artificial Intelligence Student

Project Goal:

Build a practical AI Agent capable of assisting UNSW students with course selection and study planning.

---
