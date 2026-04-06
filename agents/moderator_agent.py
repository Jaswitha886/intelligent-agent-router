from autogen_core.models import UserMessage
from config.llm_config import ollama_client
from agents.response_parser import normalize_final_text

async def moderate(pro: str, con: str, evidence: str) -> str:
    prompt = f"""
Provide a final structured decision with 3-4 comprehensive points.

Return format strictly:

Final Decision:
- Point 1:
- Point 2:
- Point 3:
- Point 4:

Final Answer:
Provide a concise, one-sentence summary conclusion.

Rules:
- Provide exactly 3-4 decision points.
- Use bullet points only, no paragraphs.
- No repetition.
- Be balanced and analytical.
- Conclude with a clear final answer.

Pro:
{pro}

Con:
{con}

Evidence:
{evidence}
"""

    response = await ollama_client.create(
        [UserMessage(content=prompt, source="user")]
    )

    final_text = normalize_final_text(response.content)
    if final_text.strip():
        return final_text

    # Retry with a stricter format if the first generation is empty/invalid.
    retry_prompt = f"""
You MUST return a comprehensive final answer now.

Rules:
- Output exactly 3-4 decision bullet points with explanations.
- Start with 'Final Decision:'.
- Follow with a one-sentence 'Final Answer:'.
- Do not leave the answer empty.
- Be concise and clear.

Final Decision:
- Point 1:
- Point 2:
- Point 3:
- Point 4:

Final Answer:

Context:
Pro:
{pro}

Con:
{con}

Evidence:
{evidence}
"""

    retry_response = await ollama_client.create(
        [UserMessage(content=retry_prompt, source="user")]
    )
    retry_final_text = normalize_final_text(retry_response.content)
    if retry_final_text.strip():
        return retry_final_text

    return "- Final answer could not be generated from the current model output."
