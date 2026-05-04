import os
import uuid
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from app.config.settings import get_settings

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)
get_settings.cache_clear()

from app.database.vector_store import VectorStore

vec = VectorStore()

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "faqs_data.csv")
df = pd.read_csv(csv_path)

texts = df["combined_text"].tolist()
embeddings = []

batch_size = 50

for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    batch_embeddings = vec.openai_client.embeddings.create(
        input=batch,
        model=vec.embedding_model
    ).data

    embeddings.extend([e.embedding for e in batch_embeddings])

records = []
for i, row in df.iterrows():
    records.append({
        "id": str(uuid.uuid4()),
        "metadata": {
            "category": row["category"],
            "created_at": datetime.now().isoformat(),
        },
        "contents": row["combined_text"],
        "embedding": embeddings[i],
    })

records_df = pd.DataFrame(records)

vec.upsert(records_df)