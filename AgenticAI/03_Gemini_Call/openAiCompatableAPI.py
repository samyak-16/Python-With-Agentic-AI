from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain to me how AI works in single sentence ."},
    ],
)


print(response.choices[0].message.content)
