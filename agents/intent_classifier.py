from autogen_core.models import UserMessage
from config.llm_config import ollama_client
from agents.response_parser import content_to_text

async def classify_intent(query: str) -> str:
    response = await ollama_client.create(
        [
            UserMessage(
                content=f"""
Classify the following query as either SIMPLE or COMPLEX.

Rules:
- Reply with only one word.
- Do not explain.

Query: {query}
""",
                source="user",
            )
        ]
    )

    return content_to_text(response.content).strip().upper()
