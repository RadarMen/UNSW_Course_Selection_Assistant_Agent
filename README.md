# UNSW Course Selection Assistant

> An LLM-powered course selection assistant that uses Retrieval-Augmented Generation (RAG) to answer questions about UNSW programs, courses, prerequisites, terms, and degree requirements.

The project provides a complete web application with a Vue frontend, a FastAPI backend, persistent user conversations, a ChromaDB knowledge base, MySQL storage, and Docker Compose deployment.

> 中文简介：一个面向 UNSW 研究生选课场景的 RAG Agent，可基于上传的 Handbook PDF 回答课程信息、先修课、开课学期和项目要求等问题。

---

## Project Overview

UNSW Handbook information is comprehensive but distributed across program pages, course pages, prerequisite descriptions, and requirement groups. Students often need to search through multiple documents before they can answer a single course-planning question.

This project converts UNSW Handbook documents into a searchable vector knowledge base and combines the retrieved information with conversation history and a large language model to provide contextual answers.

The current version supports:

- PDF handbook ingestion
- Course and program document classification
- Text splitting and embedding
- ChromaDB vector retrieval
- Question classification and targeted retrieval
- Multi-turn conversations
- User registration and login
- Multiple chat sessions per user
- Persistent chat history
- Streaming AI responses
- Vue and FastAPI integration
- MySQL data persistence
- Docker Compose deployment

---

## Current Project Status

The main MVP workflow is complete.

| Module | Status |
|---|---|
| Handbook PDF ingestion | Completed |
| Text splitting and vectorisation | Completed |
| MD5 duplicate detection | Completed |
| ChromaDB persistent storage | Completed |
| RAG question-answering chain | Completed |
| Course/program metadata filtering | Completed |
| Question classification | Completed |
| Multi-turn conversation history | Completed |
| User registration and login | Completed |
| Chat session management | Completed |
| MySQL integration | Completed |
| FastAPI backend | Completed |
| Vue 3 + Vite frontend | Completed |
| Frontend-backend integration | Completed |
| Docker image build | Completed |
| Docker Compose deployment | Completed |

---

## Key Features

### 1. UNSW Handbook Knowledge Base

The system accepts UNSW Handbook PDF files and processes them through the following pipeline:

1. Extract text from the PDF.
2. Identify whether the document describes a program or a course.
3. Generate metadata from the file name.
4. Split long text into overlapping chunks.
5. Generate vector embeddings.
6. Store vectors and metadata in ChromaDB.
7. Record the document hash to prevent duplicate ingestion.

### 2. Retrieval-Augmented Generation

For every question, the backend:

1. Receives the user query and `session_id`.
2. Analyses the type of question.
3. Applies the appropriate metadata filter.
4. Retrieves relevant handbook chunks from ChromaDB.
5. Loads the conversation history.
6. Builds a structured prompt.
7. Sends the prompt to the LLM.
8. Returns either a normal or streaming response.
9. Stores the conversation in MySQL.

### 3. User and Session Management

The application supports:

- User registration
- User login
- User-specific chat sessions
- Multiple conversations for each user
- Persistent user messages and assistant responses
- Retrieval of previous sessions and messages

Each conversation has its own `session_id`, which keeps the context of different conversations isolated.

### 4. Streaming Responses

The streaming chat interface allows the frontend to display generated text progressively rather than waiting for the full response.

### 5. Dockerised Deployment

The application can be started with a single command:

```bash
docker compose up --build
```

Docker Compose coordinates:

- Vue production build
- Nginx frontend service
- FastAPI backend service
- MySQL database service
- ChromaDB and application data persistence

---

## System Architecture

```mermaid
flowchart LR
    U[User Browser] --> N[Nginx]
    N --> F[Vue 3 Frontend]
    F -->|REST / Streaming API| B[FastAPI Backend]

    B --> A[Authentication Service]
    B --> S[Session and Message Service]
    A --> M[(MySQL)]
    S --> M

    B --> Q[Question Classifier]
    Q --> R[RAG Service]
    R --> V[(ChromaDB)]
    R --> H[Conversation History]
    R --> L[Qwen LLM API]

    P[UNSW Handbook PDF] --> E[PDF Parser]
    E --> C[Text Splitter]
    C --> D[Embedding Model]
    D --> V
```

---

## RAG Workflow

```text
User Query
    |
    v
Question Classification
    |
    v
Metadata Filter Selection
    |
    v
ChromaDB Similarity Search
    |
    v
Relevant Handbook Chunks
    |
    +--------------------+
    |                    |
    v                    v
Conversation History   User Query
    |                    |
    +---------+----------+
              |
              v
       Prompt Construction
              |
              v
          LLM Response
              |
              v
     Save Message to MySQL
```

---

## Technology Stack

### Frontend

- Vue 3
- Vite
- JavaScript
- Axios
- Nginx

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- PyMySQL
- Passlib

### AI and RAG

- LangChain
- DashScope / Qwen
- DashScope Embeddings
- ChromaDB
- Recursive text splitting
- Metadata-filtered retrieval
- Conversation-aware prompting

### Data and Deployment

- MySQL
- Docker
- Docker Compose
- Persistent volumes
- Git and GitHub

---

## Project Structure

The exact structure may change as the project continues to evolve, but the main modules are organised as follows:

```text
unsw-course-selection-agent/
├── frontend/                   # Vue 3 + Vite frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
│
├── main.py                     # FastAPI application entry point
├── database.py                 # MySQL connection and database setup
├── rag.py                      # RAG chain and prompt construction
├── knowledge_base.py           # Document ingestion and vectorisation
├── vector_stores.py            # ChromaDB vector store service
├── config_data.py              # RAG and application configuration
├── file_history_store.py       # Conversation history implementation
│
├── data/                       # Uploaded handbook documents
├── chroma_db/                  # Persistent ChromaDB data
├── chat_history/               # Local history data or compatibility storage
│
├── requirements.txt
├── Dockerfile                  # Backend Docker image
├── docker-compose.yml
├── .dockerignore
├── .env.docker                 # Local Docker environment variables
└── README.md
```

---

## Handbook File Naming Rules

File names are used to identify the document type and generate metadata.

### Program Handbook

```text
program_<program_name_or_code>_<year>.pdf
```

Examples:

```text
program_master_of_information_technology_2026.pdf
program_8543_2026.pdf
```

### Course Handbook

```text
course_<course_code>_<year>.pdf
```

Examples:

```text
course_COMP9417_2026.pdf
course_COMP9517_2026.pdf
```

### Generated Metadata

Depending on the file type, the system can generate metadata such as:

```json
{
  "university": "UNSW",
  "degree_level": "postgraduate",
  "year": 2026,
  "handbook_type": "course",
  "course_code": "COMP9417",
  "source": "course_COMP9417_2026.pdf"
}
```

Program documents use `handbook_type: "program"` and store the relevant program name or program code instead of a course code.

Consistent naming is important because metadata is used during targeted retrieval.

---

## Prerequisites

For Docker deployment:

- Docker Desktop
- Docker Compose
- A DashScope API key
- Internet access for the LLM and embedding APIs

For local development:

- Python 3.11
- Node.js and npm
- MySQL
- A DashScope API key

---

## Environment Variables

Create a `.env.docker` file in the project root.

Example:

```env
DASHSCOPE_API_KEY=your_dashscope_api_key

MYSQL_DATABASE=unsw_agent
MYSQL_USER=agent_docker
MYSQL_PASSWORD=change_this_password
MYSQL_ROOT_PASSWORD=change_this_root_password

DATABASE_URL=mysql+pymysql://agent_docker:change_this_password@mysql:3306/unsw_agent
```

Important:

- Inside Docker Compose, the database hostname should normally be the MySQL service name, such as `mysql`, rather than `127.0.0.1`.
- Do not commit `.env.docker` to GitHub.
- Add an `.env.docker.example` file containing variable names but no real secrets.
- Change all example database passwords before deployment.

Recommended `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example
!.env.docker.example

__pycache__/
*.py[cod]

node_modules/
frontend/dist/

chroma_db/
chat_history/
data/
md5.txt
```

Whether the persistent data directories should be ignored depends on whether the repository contains demonstration data.

---

## Quick Start with Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/<your-github-username>/unsw-course-selection-agent.git
cd unsw-course-selection-agent
```

### 2. Create the Environment File

```bash
cp .env.docker.example .env.docker
```

On Windows PowerShell:

```powershell
Copy-Item .env.docker.example .env.docker
```

Add your API key and database configuration to `.env.docker`.

### 3. Build and Start the Application

```bash
docker compose up --build
```

### 4. Open the Application

After all containers have started:

- Frontend: `http://127.0.0.1`
- Backend API documentation: `http://127.0.0.1:8000/docs`
- Alternative API documentation: `http://127.0.0.1:8000/redoc`

The backend listens on `0.0.0.0:8000` inside the container so that Docker can expose it to the host. From the browser on the host machine, use `127.0.0.1:8000`.

### 5. Stop the Application

```bash
docker compose down
```

To stop the containers and remove the database volume:

```bash
docker compose down -v
```

Use the second command carefully because it removes persistent Docker volumes.

---

## Useful Docker Commands

Build and start all services:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d --build
```

View service status:

```bash
docker compose ps
```

View all logs:

```bash
docker compose logs -f
```

View backend logs:

```bash
docker compose logs -f backend
```

View frontend logs:

```bash
docker compose logs -f frontend
```

View MySQL logs:

```bash
docker compose logs -f mysql
```

Restart one service:

```bash
docker compose restart backend
```

Rebuild only the backend:

```bash
docker compose up -d --build backend
```

---

## Local Development

### Backend

Create and activate a Python environment:

```bash
conda create -n pzk_env python=3.11
conda activate pzk_env
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the API key and database connection, then start FastAPI:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite development server normally starts at:

```text
http://127.0.0.1:5173
```

During local development, make sure the frontend API base URL points to the FastAPI backend.

---

## API Capabilities

The exact route list is available through FastAPI Swagger at `/docs`.

The backend currently provides route groups for:

| Capability | Description |
|---|---|
| Authentication | Register and log in users |
| User management | Create and identify application users |
| Session management | Create, list, and retrieve chat sessions |
| Message history | Store and retrieve messages by session |
| Handbook upload | Parse and ingest handbook PDF files |
| Standard chat | Return a complete RAG response |
| Streaming chat | Stream generated tokens to the frontend |

A confirmed authentication route used by the application is:

```http
POST /auth/register
```

When the frontend is served through Nginx, API requests may be proxied through an `/api` prefix:

```http
POST /api/auth/register
```

Always use `/docs` as the source of truth for the final endpoint paths and request schemas.

---

## Example Questions

After relevant handbook documents have been uploaded, the assistant can answer questions such as:

```text
What are the core course requirements for my program?
```

```text
Can I take COMP9417 without completing its prerequisite?
```

```text
Which terms is COMP9517 offered in?
```

```text
How many units of credit do I need from this course group?
```

```text
What is the difference between these two COMP courses?
```

```text
Based on the handbook, which course should I complete first?
```

---

## Data Persistence

The project contains three main types of persistent data.

### MySQL

Stores application-level structured data such as:

- Users
- Authentication information
- Chat sessions
- User messages
- Assistant messages

### ChromaDB

Stores:

- Handbook text chunks
- Vector embeddings
- Source metadata
- Course or program metadata

### Local Application Data

Depending on the current configuration, local directories may store:

- Uploaded PDF files
- MD5 document hashes
- Compatibility chat-history files
- Temporary processing data

Docker mounts or volumes should be used for these directories so that rebuilding a container does not delete the knowledge base.

---

## Retrieval Design

The system uses both semantic similarity and metadata to improve retrieval quality.

Typical question categories include:

- `prerequisite`
- `course_information`
- `program_requirement`

The category can be used to determine which document type should be searched.

For example:

```text
Question: What are the prerequisites for COMP9417?
Filter: handbook_type = course
Course code: COMP9417
```

```text
Question: How many UOC are required from the program elective group?
Filter: handbook_type = program
```

This reduces irrelevant retrieval compared with searching every document without filters.

---

## Duplicate Document Detection

Before a handbook is added to ChromaDB, the extracted document content is hashed.

```text
PDF content
    |
    v
MD5 hash
    |
    +--> Already exists: skip ingestion
    |
    +--> New document: split, embed, and store
```

This prevents the same handbook content from being embedded multiple times.

---

## Design Decisions

### Why ChromaDB?

ChromaDB provides a lightweight persistent vector database that is suitable for a local RAG application and can be integrated directly with LangChain.

### Why MySQL?

MySQL stores structured application data that should not be placed in the vector database, including users, sessions, and messages.

### Why Separate MySQL and ChromaDB?

The two databases solve different problems:

- MySQL stores structured relational data.
- ChromaDB stores embeddings and supports semantic retrieval.

### Why Use a Separate `session_id`?

A user may create multiple conversations. Each conversation needs an independent context, so every chat session receives its own unique `session_id`.

The data flow is:

```text
Create User
    |
    v
user_id
    |
    v
Create Chat Session
    |
    v
session_id
    |
    v
Send and Store Messages
```

### Why Docker Compose?

The application depends on multiple services. Docker Compose provides a reproducible environment for the frontend, backend, and database and reduces local configuration differences.

---

## Known Limitations

- Answers depend on the uploaded handbook documents.
- Missing or outdated documents can lead to incomplete answers.
- Semantic retrieval does not guarantee that every relevant rule is retrieved.
- LLM-generated answers can contain mistakes.
- Program rules with complex nested conditions may require a future deterministic rule engine.
- The project does not replace official academic advice or enrolment approval.
- Course availability, prerequisites, and program rules should be verified against the official UNSW Handbook.

---

## Roadmap

Potential future improvements include:

- Automatic synchronisation with updated UNSW Handbook data
- Structured program-rule validation
- Automatic prerequisite graph construction
- Timetable conflict detection
- Degree progress tracking
- Course recommendation scoring
- Hybrid keyword and vector retrieval
- Reranking retrieved chunks
- Automated tests for API and RAG behaviour
- GitHub Actions CI/CD
- Cloud deployment
- Monitoring and logging
- Improved citation display in generated answers

---

## Testing Checklist

Before publishing a new version, verify:

- [ ] A new user can register.
- [ ] An existing user can log in.
- [ ] A user can create multiple chat sessions.
- [ ] Messages remain isolated by `session_id`.
- [ ] A course PDF can be uploaded.
- [ ] A program PDF can be uploaded.
- [ ] Duplicate documents are rejected or skipped.
- [ ] Course questions retrieve course documents.
- [ ] Program questions retrieve program documents.
- [ ] Standard chat responses work.
- [ ] Streaming responses work.
- [ ] Chat history remains available after restarting the backend.
- [ ] MySQL data remains available after restarting containers.
- [ ] ChromaDB data remains available after rebuilding containers.
- [ ] The frontend can access the backend through Nginx.
- [ ] `docker compose up --build` starts the full application successfully.

---

## Security Notes

- Never commit API keys, database passwords, or production secrets.
- Use environment variables for sensitive configuration.
- Replace development database credentials before public deployment.
- Limit accepted upload file types and file sizes.
- Validate uploaded file names before using them as metadata.
- Configure production CORS rules explicitly.
- Use HTTPS when deploying outside a local development environment.

---

## Disclaimer

This project is an independent educational and portfolio project. It is not an official UNSW service.

The assistant is designed to help users locate and understand information from uploaded handbook documents. It does not guarantee that an answer is complete or current. Users should verify important academic decisions with the official UNSW Handbook and, where necessary, UNSW academic advisers.

---

## Author

Developed as an AI and software engineering portfolio project by a UNSW Master of Information Technology student specialising in Artificial Intelligence.

---

## Acknowledgements

- UNSW Handbook content used as the project knowledge source
- LangChain for RAG orchestration
- ChromaDB for vector storage
- Alibaba Cloud DashScope for embedding and language models
- FastAPI, Vue, MySQL, Docker, and Nginx for the full-stack application
