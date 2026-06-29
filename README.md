# CamTech University Chatbot [Project Base Learning]

A highly capable conversational chatbot designed for CamTech University, built using a modern Retrieval-Augmented Generation (RAG) architecture. The chatbot allows users to query information naturally, retaining conversational context across interactions.

## 🌟 Key Features

*   **Conversational Memory**: Remembers past interactions within a session for natural back-and-forth conversations.
*   **RAG Architecture**: Leverages vector embeddings to provide accurate, context-aware answers based on institutional data.
*   **Vector Database**: Uses PostgreSQL with the `pgvector` extension for efficient and scalable semantic search.
*   **Multi-Interface Support**: Provides both a Command-Line Interface (CLI) for testing and a FastAPI backend for web integration.
*   **Modern Python Tooling**: Managed with `uv` for lightning-fast dependency resolution and isolated environments.

## 🛠️ Technology Stack

*   **Language**: Python 3.12+
*   **Frameworks**: [LangChain](https://python.langchain.com/) for LLM orchestration, [FastAPI](https://fastapi.tiangolo.com/) for the API.
*   **Database**: PostgreSQL with `pgvector` (via Docker).
*   **Package Management**: `uv`.
*   **Containerization**: Docker & Docker Compose.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

*   [Python 3.12+](https://www.python.org/downloads/)
*   [Docker](https://docs.docker.com/get-docker/) & Docker Compose
*   [uv](https://docs.astral.sh/uv/) (Python package manager)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd camtech_chatbot
```

### 2. Environment Setup

Create a `.env` file in the root directory and configure your necessary API keys and database credentials. You can use the provided `.env` if available or set up variables like your LLM provider keys (e.g., Google GenAI, Groq).

### 3. Start the Vector Database

The project uses Docker Compose to easily spin up a PostgreSQL instance pre-configured with `pgvector`.

```bash
docker-compose up -d
```
*Note: This runs the database on port `5432`.*

### 4. Install Dependencies

Use `uv` to sync the project dependencies:

```bash
uv sync
```

### 5. Running the Application

You can interact with the chatbot in two ways:

#### Option A: Command Line Interface (Interactive)
To launch the terminal-based chat session, run:
```bash
uv run python main.py
```
Type your questions directly in the terminal, and type `exit` or `quit` to end the conversation.

#### Option B: REST API (FastAPI)
To start the backend API server, you can run the Docker container or use uvicorn directly:
```bash
uv run uvicorn src.api.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.

Alternatively, build and run the entire application via Docker:
```bash
docker build -t camtech-chatbot .
docker run -p 8000:8000 camtech-chatbot
```

## 📁 Project Structure

```text
camtech_chatbot/
├── .env                  # Environment variables and API keys
├── docker-compose.yml    # Defines the PostgreSQL vector database
├── Dockerfile            # Instructions for containerizing the API
├── main.py               # Entry point for the CLI conversational bot
├── pyproject.toml        # Project metadata and dependencies (uv)
├── uv.lock               # Dependency lockfile
└── src/
    ├── api/              # FastAPI application and endpoints
    ├── bot/              # LangChain RAG setup and chains
    ├── ingestion/        # Scripts to process and load data into pgvector
    └── config.py         # Application configuration
```
