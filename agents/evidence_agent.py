from autogen_core.models import UserMessage
from config.llm_config import ollama_client
from agents.response_parser import normalize_evidence_text

async def evaluate_evidence(pro: str, con: str) -> str:
    prompt = f"""
Evaluate both sides and extract structured insights with 3-4 points each.

Return format:

Supporting Evidence:
- Point 1:
- Point 2:
- Point 3:
- Point 4:

Limitations & Contradictions:
- Point 1:
- Point 2:
- Point 3:
- Point 4:

Rules:
- Provide 3-4 points for each section.
- Use bullet points only, no paragraphs.
- Be analytical and balanced.
- Be concise but substantive.

Pro:
{pro}

Con:
{con}
"""

    response = await ollama_client.create(
        [UserMessage(content=prompt, source="user")]
    )

    return normalize_evidence_text(response.content)
