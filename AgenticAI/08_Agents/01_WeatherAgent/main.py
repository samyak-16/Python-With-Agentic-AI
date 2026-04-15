from openai import OpenAI
from dotenv import load_dotenv
import requests


load_dotenv()


client = OpenAI()


def extract_weather(city: str):
    res = requests.get(f"https://wttr.in/{city.lower()}?format=%C+%t")
    res.encoding = "utf-8"
    if res.status_code == 200:
        return f"The weather for {city.lower()} is {res.text}"
    else:
        return "Something wen't wrong"


def main():
    query = input("> ")
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": query}]
    )

    print(f"🤖: {response.choices[0].message.content}")


# main()

print(extract_weather("biratnagar"))
