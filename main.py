import asyncio
from agents.intent_classifier import classify_intent
from router.query_router import route
from orchestrator.debate_controller import run_debate
from agents.moderator_agent import moderate
from config.llm_config import ollama_client

async def main():
    query = input("Enter your query: ")

    intent = await classify_intent(query)
    mode = route(intent)

    if mode == "single":
        result = await moderate(query, "", "")
    else:
        result = await run_debate(query)

    print("\nFinal Answer:\n")
    print(result)

    await ollama_client.close()

if __name__ == "__main__":
    asyncio.run(main())
