from autogen_core.models import UserMessage
from config.llm_config import ollama_client
from agents.response_parser import normalize_pro_text

async def pro_reason(query: str) -> str:
    response = await ollama_client.create(
        [
            UserMessage(
                content=f"""
Provide 3-4 clear, detailed bullet points supporting the following statement:

{query}

Rules:
- You MUST provide exactly 3-4 pros.
- Use bullet points with detailed explanations.
- No paragraphs, only bullet points.
- Each point should be substantive and clear.
- Be concise but comprehensive.

Supporting Points:
- Point 1:
- Point 2:
- Point 3:
- Point 4:
""",
                source="user",
            )
        ]
    )

    return normalize_pro_text(response.content)
