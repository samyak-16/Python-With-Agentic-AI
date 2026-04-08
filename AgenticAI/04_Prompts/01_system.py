from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI(
    api_key="AIzaSyA3F00LuqdraOwFMifTLKiXFhyR65EY7Rg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful math assistant and only and only answer math related questions.",
        },
        {
            "role": "user",
            # "content": "Explain to me how AI works in single sentence in context of mathmatics .",
            # "content": "Hey I'm Samyak Raj Subedi . Who are you ?",
            # "content": "Hey can you code a python program that can print hello",
            "content": "Hey can you give me the formula of (a+b)^2",
        },
    ],
)


print(response.choices[0].message.content)
