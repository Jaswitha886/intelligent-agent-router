def route(intent: str) -> str:
    return "single" if intent == "SIMPLE" else "debate"
