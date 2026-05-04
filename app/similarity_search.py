from app.database.vector_store import VectorStore
from app.services.synthesizer import Synthesizer

vec = VectorStore()

relevant_question = "إيه هي طرق التوصيل وكم يستغرق الشحن للمحافظات؟"
results = vec.search(relevant_question, limit=3, return_dataframe=False)

response = Synthesizer.generate_response(question=relevant_question, context=results)
print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

irrelevant_question = "مين كسب الماتش إمبارح؟"
results = vec.search(irrelevant_question, limit=3, return_dataframe=False)

response = Synthesizer.generate_response(question=irrelevant_question, context=results)
print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

metadata_filter = {"category": {"$eq": "الشحن"}}
results = vec.search(
    relevant_question,
    limit=3,
    metadata_filter=metadata_filter,
    return_dataframe=False,
)

response = Synthesizer.generate_response(question=relevant_question, context=results)
print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

multi_filter = {"$or": [{"category": {"$eq": "الشحن"}}, {"category": {"$eq": "الدفع"}}]}
results = vec.search(
    relevant_question,
    limit=3,
    metadata_filter=multi_filter,
    return_dataframe=False,
)

combined_filter = {
    "$and": [
        {"category": {"$eq": "الشحن"}},
        {"created_at": {"$gt": "2026-05-01"}},
    ]
}
results = vec.search(
    relevant_question,
    limit=3,
    metadata_filter=combined_filter,
    return_dataframe=False,
)