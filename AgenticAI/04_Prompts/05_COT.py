# COT : Chain Of Thought

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # Reading the .env file and setting it in the environment

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using Chain of thouoght. 
You work on START , PLAN and OUTPUT steps .
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
ONCE you think enough PLAN has been done , finally you can give an OUTPUT .

Rules : 
    - Strictly follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives a input) , PLAN(That can be multiple times) and Finally OUTPUT(which is going to be displayes to the user).

    Output JSON Format:
    {{"step":"START" | "PLAN" |"OUTPUT" ,
        "content":"string" }}

    Example : 

    Q: Hey, Can you solve 2 + 3 * 5 / 10
    START : Hey , can you solve  2 + 3 * 5 / 10
    PLAN : {"step" : "PLAN" , "content":"Seems Like user is interested in math problem"}
    PLAN : {"step" : "PLAN" , "content":"Looking at the problem, we should solve this using BODMAS method"}
    PLAN : {"step" : "PLAN" , "content":"Yes ,  BODMAS is the correct thing to do here "}
    PLAN : {"step" : "PLAN" , "content":"First we muntiply 3*5 which is 15"}
    PLAN : {"step" : "PLAN" , "content":"Now the equation is 2 + 15/10"}
    PLAN : {"step" : "PLAN" , "content":"We must perform divide that is 15/10 is 1.5"}
    PLAN : {"step" : "PLAN" , "content":"Finally let's perform addition "}
    PLAN : {"step" : "PLAN" , "content":"Great, we have solved and final answer is 3.5 "}
    OUTPUT : {"step" : "OUTPUT" , "content":"3.5"}

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
            "content": "Hey can you write a python code to check is number is even or odd",
        },
    ],
)


print(response.choices[0].message.content)
