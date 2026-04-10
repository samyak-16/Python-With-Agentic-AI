from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI()

client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hey There"},
    ],
)
