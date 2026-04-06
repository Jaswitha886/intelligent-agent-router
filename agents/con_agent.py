from autogen_core.models import UserMessage
from config.llm_config import ollama_client
from agents.response_parser import normalize_con_text

async def con_reason(query: str) -> str:
    response = await ollama_client.create(
        [
            UserMessage(
                content=f"""
Provide 3-4 clear, detailed bullet points opposing the following statement:

{query}

Rules:
- You MUST provide exactly 3-4 cons.
- Use bullet points with detailed explanations.
- No paragraphs, only bullet points.
- Each point should be substantive and analytical.
- Be concise but comprehensive.
- Be critical and direct.

Opposing Points:
- Point 1:
- Point 2:
- Point 3:
- Point 4:
""",
                source="user",
            )
        ]
    )

    return normalize_con_text(response.content)
