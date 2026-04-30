from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333},
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-mini",
            "temperature": 0.1,
            "api_key": OPEN_API_KEY,
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"},
        "api_key": OPEN_API_KEY,
    },
    # "reranker": {
    #     "provider": "cohere",
    #     "config": {"model": "rerank-english-v3.0"},
    # },
}

memory = Memory.from_config(config)

while True:
    user_query = input("> ")
    search_memories = memory.search(query=user_query, filters={"user_id": "Samyak"})
    # print(search_memories)
    memory_str = "\n".join([m["memory"] for m in search_memories["results"]])
    # print(memory_str)
    SYSTEM_PROMPT = f"Relevant memories about this user:\n{memory_str}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    ai_response = response.choices[0].message.content

    print("AI : ", ai_response)

    memory.add(
        user_id="Samyak",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response},
        ],
    )

    print("Memory has been saved :)")
