from typing import Any, Dict, Iterable, List, Tuple
from pydantic import BaseModel, Field
from app.services.llm_factory import LLMFactory

class SynthesizedResponse(BaseModel):
    thought_process: List[str] = Field(
        description="List of thoughts that the AI assistant had while synthesizing the answer"
    )
    answer: str = Field(description="The synthesized answer to the user's question")
    enough_context: bool = Field(
        description="Whether the assistant has enough context to answer the question"
    )

class Synthesizer:
    SYSTEM_PROMPT = """
    # Role and Purpose
    You are an AI assistant for an e-commerce FAQ system. Your task is to synthesize a coherent and helpful answer 
    based on the given question and relevant context retrieved from a knowledge database.

    # Guidelines:
    1. Provide a clear and concise answer to the question.
    2. Use only the information from the relevant context to support your answer.
    3. The context is retrieved based on cosine similarity, so some information might be missing or irrelevant.
    4. Be transparent when there is insufficient information to fully answer the question.
    5. Do not make up or infer information not present in the provided context.
    6. If you cannot answer the question based on the given context, clearly state that.
    7. Maintain a helpful and professional tone appropriate for customer service.
    8. Adhere strictly to company guidelines and policies by using only the provided knowledge base.
    """

    @staticmethod
    def generate_response(
        question: str,
        context: List[Tuple[Any, ...]],
        provider: str = "openai",
    ) -> SynthesizedResponse:
        """Generates a synthesized response based on the question and context.

        Args:
            question: The user's question.
            context: The relevant context retrieved from the knowledge base.
            provider: The LLM provider to use (default: 'openai').

        Returns:
            A SynthesizedResponse containing thought process and answer.
        """
        context_str = Synthesizer.build_context_text(context)

        messages = [
            {"role": "system", "content": Synthesizer.SYSTEM_PROMPT},
            {
                "role": "user", 
                "content": f"# Retrieved information (Context):\n{context_str}\n\n# User question:\n{question}"
            },
        ]

        llm = LLMFactory(provider)
        return llm.create_completion(
            response_model=SynthesizedResponse,
            messages=messages,
        )

    @staticmethod
    def build_context_text(
        context: Iterable[Tuple[Any, ...]],
    ) -> str:
        """
        Convert vecs search results (list of tuples) into a readable context string.

        Each tuple is expected to be (id, distance, metadata_dict).
        """
        snippets: List[str] = []
        for record in context:
            if len(record) < 3 or not isinstance(record[2], dict):
                continue
            metadata: Dict[str, Any] = record[2]
            text = metadata.get("contents") or metadata.get("text") or ""
            if not text:
                continue
            category = metadata.get("category")
            if category:
                snippets.append(f"- {text}\n  category: {category}")
            else:
                snippets.append(f"- {text}")

        return "\n".join(snippets) if snippets else "(no relevant context found)"