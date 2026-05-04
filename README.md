# E-commerce Customer Support RAG System

## Overview

This project is an advanced Retrieval-Augmented Generation (RAG) system designed to automate customer support for e-commerce platforms. The system utilizes a modular architecture to provide accurate, context-aware responses based on a proprietary knowledge base. It features a high-performance Semantic Router for real-time query classification and metadata filtering.

## Key Features

- **Semantic Routing**: Mathematical intent classification using cosine similarity to route queries to specific categories without additional LLM latency.
- **Metadata Filtering**: Precision retrieval using PostgreSQL with Timescale Vector to filter results by category (e.g., Shipping, Payments, Returns).
- **Structured Output**: Strict data validation using the `instructor` library to ensure consistent JSON responses.
- **Hybrid LLM Support**: Factory pattern implementation to switch between OpenAI and Anthropic models seamlessly.
- **Asynchronous API**: Built with FastAPI for high-concurrency performance and production-ready deployment.

## Tech Stack

- **Backend**: Python 3.10+, FastAPI.
- **Database**: PostgreSQL with Timescale Vector extension.
- **AI Models**: OpenAI (GPT-4o, Text-Embedding-3-Small), Anthropic (Claude 3.5 Sonnet).
- **Orchestration**: Instructor, Pydantic, NumPy.
- **Package Management**: `uv` (Astral).
- **Deployment**: Docker, Hugging Face Spaces.

## Project Structure

```plaintext
├── app/
│   ├── api.py              # FastAPI endpoints and middleware configuration
│   ├── config/
│   │   └── settings.py     # Environment variables and Pydantic settings
│   ├── database/
│   │   └── vector_store.py # Vector operations and semantic routing logic
│   ├── services/
│   │   ├── llm_factory.py  # Provider-agnostic LLM integration
│   │   ├── synthesizer.py  # RAG logic and response generation
│   │   └── classifier.py   # Intent classification service
├── Dockerfile              # Containerization for Hugging Face deployment
├── pyproject.toml          # Project dependencies and metadata
└── .env                    # Configuration for API keys and database URLs
```

## Installation and Setup

### Prerequisites

- Python 3.10 or higher.
- `uv` package manager.
- PostgreSQL instance with Timescale Vector enabled.

### Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
OPENAI_API_KEY=your_openai_key
TIMESCALE_SERVICE_URL=postgresql://USER:PASSWORD@HOST.pooler.supabase.com:6543/DB
```

### Setup Steps

1. Clone the repository.
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
3. Run the development server:
   ```bash
   uv run uvicorn app.api:app --reload
   ```

## API Reference

### Chat Endpoint

- **URL**: `/api/chat`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "question": "What are your international shipping rates?",
    "provider": "openai",
    "filters": { "category": "Shipping" }
  }
  ```
- **Response**: Returns a structured JSON containing the `answer`, `thought_process`, `predicted_category`, and a boolean `enough_context` flag.

## Deployment on Hugging Face Spaces

This project is optimized for deployment as a Docker Space on Hugging Face.

### Deployment Steps

1. **Create a New Space**: Choose "Docker" as the Space type.
2. **Configure Secrets**: In the Space settings, add the following variables as **Secrets**:
   - `OPENAI_API_KEY`
   - `TIMESCALE_SERVICE_URL`
3. **Push to Hub**: Push your code to the Hugging Face Space repository.
4. **Platform Requirements**:
   - The `Dockerfile` uses port `7860` as required by Hugging Face.
   - It runs under a non-root user (UID 1000) for security.
   - It uses `uv` for extremely fast build times.

```bash
# Example of building locally to test
docker build -t rag-api .
docker run -p 7860:7860 --env-file .env rag-api
```
