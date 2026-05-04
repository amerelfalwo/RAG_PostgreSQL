import logging
import time
from typing import Any, List, Optional, Tuple, Union

import pandas as pd
from app.config.settings import get_settings
from openai import OpenAI
from vecs import create_client


class VectorStore:

    def __init__(self):
        self.settings = get_settings()
        self.openai_client = OpenAI(
            api_key=self.settings.openai.api_key,
            base_url=self.settings.openai.base_url
        )
        self.embedding_model = self.settings.openai.embedding_model
        self.vector_settings = self.settings.vector_store
        self.vec_client = create_client(self.settings.database.service_url)
        self.collection = self.vec_client.get_or_create_collection(
            name=self.vector_settings.table_name,
            dimension=self.vector_settings.embedding_dimensions,
        )

    def get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        start_time = time.time()
        embedding = (
            self.openai_client.embeddings.create(
                input=[text],
                model=self.embedding_model,
            )
            .data[0]
            .embedding
        )
        elapsed_time = time.time() - start_time
        logging.info(f"Embedding generated in {elapsed_time:.3f} seconds")
        return embedding

    def create_tables(self) -> None:
        pass

    def create_index(self) -> None:
        self.collection.create_index()

    def drop_index(self) -> None:
        pass

    def upsert(self, df: pd.DataFrame) -> None:
        records = []
        for _, row in df.iterrows():
            metadata = row.get("metadata", {})
            if "contents" in row:
                metadata["contents"] = row["contents"]
            records.append((str(row["id"]), row["embedding"], metadata))
        self.collection.upsert(records=records)
        logging.info(
            f"Inserted {len(df)} records into {self.vector_settings.table_name}"
        )

    def search(
        self,
        query_text: str,
        limit: int = 5,
        metadata_filter: Union[dict, List[dict]] = None,
        return_dataframe: bool = True,
    ) -> Union[List[Tuple[Any, ...]], pd.DataFrame]:
        query_embedding = self.get_embedding(query_text)
        start_time = time.time()

        search_args = {
            "data": query_embedding,
            "limit": limit,
            "include_value": True,
            "include_metadata": True,
        }

        if metadata_filter and isinstance(metadata_filter, dict) and len(metadata_filter) > 0:
            search_args["filters"] = metadata_filter

        results = self.collection.query(**search_args)
        logging.info("Query embedding head (first 5): %s", query_embedding[:5])
        logging.info("Raw vecs results: %s", results)
        elapsed_time = time.time() - start_time
        logging.info(f"Vector search completed in {elapsed_time:.3f} seconds")

        if return_dataframe:
            return self._create_dataframe_from_results(results)
        return results

    def _create_dataframe_from_results(
        self,
        results: List[Tuple[Any, ...]],
    ) -> pd.DataFrame:
        formatted_results = []
        for r in results:
            id_val = r[0]
            distance = r[1]
            metadata = r[2] if len(r) > 2 else {}
            contents = metadata.get("contents", "")
            formatted_results.append((id_val, metadata, contents, None, distance))

        df = pd.DataFrame(
            formatted_results,
            columns=["id", "metadata", "contents", "embedding", "distance"]
        )

        if not df.empty:
            df = pd.concat(
                [df.drop(["metadata"], axis=1), df["metadata"].apply(pd.Series)], axis=1
            )

        df["id"] = df["id"].astype(str)
        return df

    def delete(
        self,
        ids: List[str] = None,
        metadata_filter: dict = None,
        delete_all: bool = False,
    ) -> None:
        if sum(bool(x) for x in (ids, metadata_filter, delete_all)) != 1:
            raise ValueError(
                "Provide exactly one of: ids, metadata_filter, or delete_all"
            )

        if delete_all:
            self.collection.delete(filters={})
            logging.info(f"Deleted all records from {self.vector_settings.table_name}")
        elif ids:
            self.collection.delete(ids=ids)
            logging.info(
                f"Deleted {len(ids)} records from {self.vector_settings.table_name}"
            )
        elif metadata_filter:
            self.collection.delete(filters=metadata_filter)
            logging.info(
                f"Deleted records matching metadata filter from {self.vector_settings.table_name}"
            )
