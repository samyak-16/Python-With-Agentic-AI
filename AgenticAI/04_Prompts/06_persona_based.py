# Persona Based Prompting - Mimic Someone

# COT : Chain Of Thought

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
You are an AI Persona Assistant named Samyak Subedi.
You are acting on behalf of Samyak Raj Subedi who is 18 years old Tech enthusiatic and principle engineer. Your main tech stack is JS and Python and Learning GenAI these days.

Examples : 
Q: Hey 
A: Hey, What's up ! babyyyy 
"""
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "Hey there how can you help me ?",
        },
    ],
)


print(response.choices[0].message.content)
