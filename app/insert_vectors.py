import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from config.settings import get_settings

# Force reload of environment and clear cache in case running interactively
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)
get_settings.cache_clear()

from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
df = pd.read_csv("../data/faq_dataset.csv", sep=";")
df

# Prepare data for insertion
def prepare_record(row):

    content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )


records_df = df.apply(prepare_record, axis=1)

# Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)
