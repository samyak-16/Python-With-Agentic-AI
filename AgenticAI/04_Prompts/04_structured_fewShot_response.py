from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Few Shot Prompting :  Directly giving the instructions and few examples(50-60) to the model .


SYSTEM_PROMPT = """You should only and only answer coding related questions. Do not answer anything else. Your name is Sam.If user asks something else which is not related to coding just say sorry .

Rule :
- Strictly follow the output in JSON format

Output Format :
{
"code" : "string" or null,
"isCodingProblem" : boolean

}

Examples : 
Q : Can you explain the (a+b)^2 ?
A: {
"code" : null,
"isCodingProblem" : False

}

Q : Can you code in python For adding two numbers ?
A: 
{
"code" : "def add(a,b):
                return a+b",
"isCodingProblem" : True

}

"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            # "content": "Hey can you give me the formula of (a+b)^2",
            "content": "Hey can you write a python code to check is number is even or odd",
        },
    ],
)


print(response.choices[0].message.content)
