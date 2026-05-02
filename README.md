# RAG System with PostgreSQL and GitHub Models

This project aims to build a robust and simplified Retrieval-Augmented Generation (RAG) system.
The core idea is to use **PostgreSQL** with the `pgvectorscale` extension to store text and convert it into vector embeddings for fast and highly efficient similarity search. Furthermore, we leverage **GitHub Models** to handle the AI embedding generation.

## How it Works:
- We process textual data and convert it into numerical representations (Embeddings) using the `text-embedding-3-small` model via **GitHub Models**.
- These vectors are stored in a **PostgreSQL** database.
- When a user asks a question, the system converts the question into a vector and performs a similarity search against the database to retrieve the most relevant context and provide an accurate answer.

## Core Technologies Used:
1. **GitHub Models**: Used to generate embeddings using the OpenAI API interface, utilizing your personal GitHub Token (PAT).
2. **PostgreSQL**: The primary relational database used to store our documents and vectors.
3. **Pgvectorscale**: An advanced extension for PostgreSQL that dramatically speeds up Approximate Nearest Neighbor (ANN) searches and similarity matching.
4. **Docker**: Used to easily containerize and run the database environment without complex local setup.

## Setup Instructions:
1. Copy the `app/example.env` file and rename it to `app/.env`.
2. Open `app/.env` and insert your **GitHub Personal Access Token (PAT)** into the `OPENAI_API_KEY` variable. (The `OPENAI_BASE_URL` is already set to the GitHub Models endpoint).
3. Start the database environment using Docker:
   ```bash
   docker compose up -d
   ```
4. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. To process your data and insert it into the database, run:
   ```bash
   python app/insert_vectors.py
   ```
6. To perform a similarity search and test the system, run:
   ```bash
   python app/similarity_search.py
   ```
