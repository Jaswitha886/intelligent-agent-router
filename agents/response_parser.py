import re
from typing import Any, Iterable


def content_to_text(content: Any) -> str:
    """Normalize Ollama/AutoGen content payloads to plain text."""
    if content is None:
        return ""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        return _join_parts(content)

    if isinstance(content, dict):
        for key in ("text", "content", "message"):
            if key in content:
                return content_to_text(content[key])
        return str(content).strip()

    if hasattr(content, "text"):
        return content_to_text(getattr(content, "text"))

    if hasattr(content, "content"):
        return content_to_text(getattr(content, "content"))

    return str(content).strip()


def extract_section(text: str, aliases: list[str]) -> str | None:
    """Extract one named section from markdown-like model output."""
    if not text.strip():
        return None

    labels = [re.escape(name) for name in aliases]
    label_pattern = "|".join(labels)

    heading_re = re.compile(
        rf"^\s*(?:#+\s*)?(?P<label>{label_pattern})\s*[:\-]?\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

    match = heading_re.search(text)
    if not match:
        return None

    start = match.end()
    next_heading_re = re.compile(
        r"^\s*(?:#+\s*)?[A-Za-z][A-Za-z ]{1,50}\s*[:\-]?\s*$",
        re.MULTILINE,
    )
    next_match = next_heading_re.search(text, start)
    end = next_match.start() if next_match else len(text)

    section = text[start:end].strip()
    return section or None


def normalize_pro_text(content: Any) -> str:
    text = content_to_text(content)
    extracted = extract_section(text, ["pro", "pros", "supporting points"])
    return _clean_inline_label(extracted or text, ["pro", "pros"])


def normalize_con_text(content: Any) -> str:
    text = content_to_text(content)
    extracted = extract_section(text, ["con", "cons", "opposing points"])
    return _clean_inline_label(extracted or text, ["con", "cons"])


def normalize_evidence_text(content: Any) -> str:
    text = content_to_text(content)

    supporting = extract_section(text, ["supporting evidence", "evidence for", "supporting points"])
    limitations = extract_section(text, ["limitations", "counter evidence", "weaknesses"])

    if supporting or limitations:
        blocks: list[str] = []
        if supporting:
            blocks.append(f"Supporting Evidence:\n{supporting.strip()}")
        if limitations:
            blocks.append(f"Limitations:\n{limitations.strip()}")
        return "\n\n".join(blocks).strip()

    return text


def normalize_final_text(content: Any) -> str:
    text = content_to_text(content)
    extracted = extract_section(
        text,
        ["final decision", "final answer", "decision", "conclusion"],
    )
    return _clean_inline_label(extracted or text, ["final decision", "final answer"])


def _join_parts(parts: Iterable[Any]) -> str:
    chunks: list[str] = []
    for item in parts:
        normalized = content_to_text(item)
        if normalized:
            chunks.append(normalized)
    return "\n".join(chunks).strip()


def _clean_inline_label(text: str, labels: list[str]) -> str:
    pattern = "|".join(re.escape(label) for label in labels)
    cleaned = re.sub(rf"^\s*(?:{pattern})\s*[:\-]\s*", "", text, flags=re.IGNORECASE)
    return cleaned.strip()