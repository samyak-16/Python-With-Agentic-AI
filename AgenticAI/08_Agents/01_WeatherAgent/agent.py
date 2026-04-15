# COT : Chain Of Thought — Pydantic parsed version

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal, Optional, List
import requests

load_dotenv()

client = OpenAI()

# --- Pydantic model matching the JSON schema in the prompt ---


class COTResponse(BaseModel):
    step: Literal["START", "PLAN", "TOOL", "OBSERVE", "OUTPUT"]
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None  # populated in OBSERVE step


# --- Tool ---


def extract_weather(city: str) -> str:
    res = requests.get(f"https://wttr.in/{city.lower()}?format=%C+%t")
    res.encoding = "utf-8"
    if res.status_code == 200:
        return f"The weather for {city} is {res.text}"
    return "Something went wrong while calling the tool"


tool_list = {"extract_weather": extract_weather}


def execute_tool(tool_name: str, tool_input: str) -> str:
    return tool_list[tool_name](tool_input)


# --- System prompt (same as before) ---


SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using Chain of thouoght.
You work on START , PLAN and OUTPUT steps .
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
ONCE you think enough PLAN has been done , finally you can give an OUTPUT .
You can also call a tool if required from the list of available tools.
For every tool call wait for the observe step which is the output from the called tool

Rules :
    - Strictly follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives a input) , PLAN(That can be multiple times) and Finally OUTPUT(which is going to be displayes to the user).

    Output JSON Format:
    {{"step":"START" | "PLAN" |"TOOL" |"OBSERVE"| "OUTPUT" ,
        "content":"string" , "tool":"string" , input:"string"}}
    Available Tools :
    - extract_weather(city) : takes city name as an input string and returns the weather info about the city

    Example 1:

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

    Example 2:

    Q: Hey, What is the weather of biratnagar ?
    START :  What is the weather of biratnagar ?
    PLAN : {"step" : "PLAN" , "content":"Seems Like user is interested in weather infor of biratnagar city"}
    PLAN : {"step" : "PLAN" , "content":"Since i don't have access to live , current weather info So, looking for any available tools which might be helpful for fetching weather with city name ."}
    PLAN : {"step" : "PLAN" , "content":"Great ,  I found a tool called extract_weather which takes city name as input"}
    PLAN : {"step" : "PLAN" , "content":"I need to call extract_weather tool for biratnagar as input for city"}
    PLAN : {"step" : "TOOL" ,"tool":"extract_weather" "input":"biratnagar"}
    PLAN : {"step" : "OBSERVE" ,"tool":'extract_weather', "output":"The weather for biratnagar is Clear +26°C"}
    PLAN : {"step" : "PLAN" , "Great I got the weather info about biratnagar using the tool extract_weather"}
    OUTPUT : {"step" : "OUTPUT" , "content":"The current weather in biratnagar is 26 degree Celcius with clear sky"}

"""

# --- Main loop ---

user_input = input("> ")
messages: List = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input},
]

while True:
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        response_format=COTResponse,  # <-- Pydantic model directly
        messages=messages,
    )

    result: COTResponse = response.choices[0].message.parsed  # fully typed object
    print(f"🤖 : {result}")

    # Serialize back to JSON string for message history
    messages.append({"role": "assistant", "content": result.model_dump_json()})

    if result.step == "TOOL":
        tool_output = execute_tool(result.tool, result.input)
        observe = COTResponse(step="OBSERVE", output=tool_output)
        messages.append({"role": "user", "content": observe.model_dump_json()})

    elif result.step == "OUTPUT":
        print("Final Answer:", result.content)
        break


# # COT : Chain Of Thought unparsed version

# from openai import OpenAI
# from dotenv import load_dotenv
# import json
# from typing import List
# import requests


# load_dotenv()  # Reading the .env file and setting it in the environment

# client = OpenAI()

# SYSTEM_PROMPT = """
# You're an expert AI Assistant in resolving user queries using Chain of thouoght.
# You work on START , PLAN and OUTPUT steps .
# You need to first PLAN what needs to be done. The PLAN can be multiple steps.
# ONCE you think enough PLAN has been done , finally you can give an OUTPUT .
# You can also call a tool if required from the list of available tools.
# For every tool call wait for the observe step which is the output from the called tool

# Rules :
#     - Strictly follow the given JSON output format
#     - Only run one step at a time.
#     - The sequence of steps is START (where user gives a input) , PLAN(That can be multiple times) and Finally OUTPUT(which is going to be displayes to the user).

#     Output JSON Format:
#     {{"step":"START" | "PLAN" |"TOOL" |"OBSERVE"| "OUTPUT" ,
#         "content":"string" , "tool":"string" , input:"string"}}
#     Available Tools :
#     - extract_weather(city) : takes city name as an input string and returns the weather info about the city

#     Example 1:

#     Q: Hey, Can you solve 2 + 3 * 5 / 10
#     START : Hey , can you solve  2 + 3 * 5 / 10
#     PLAN : {"step" : "PLAN" , "content":"Seems Like user is interested in math problem"}
#     PLAN : {"step" : "PLAN" , "content":"Looking at the problem, we should solve this using BODMAS method"}
#     PLAN : {"step" : "PLAN" , "content":"Yes ,  BODMAS is the correct thing to do here "}
#     PLAN : {"step" : "PLAN" , "content":"First we muntiply 3*5 which is 15"}
#     PLAN : {"step" : "PLAN" , "content":"Now the equation is 2 + 15/10"}
#     PLAN : {"step" : "PLAN" , "content":"We must perform divide that is 15/10 is 1.5"}
#     PLAN : {"step" : "PLAN" , "content":"Finally let's perform addition "}
#     PLAN : {"step" : "PLAN" , "content":"Great, we have solved and final answer is 3.5 "}
#     OUTPUT : {"step" : "OUTPUT" , "content":"3.5"}

#     Example 2:

#     Q: Hey, What is the weather of biratnagar ?
#     START :  What is the weather of biratnagar ?
#     PLAN : {"step" : "PLAN" , "content":"Seems Like user is interested in weather infor of biratnagar city"}
#     PLAN : {"step" : "PLAN" , "content":"Since i don't have access to live , current weather info So, looking for any available tools which might be helpful for fetching weather with city name ."}
#     PLAN : {"step" : "PLAN" , "content":"Great ,  I found a tool called extract_weather which takes city name as input"}
#     PLAN : {"step" : "PLAN" , "content":"I need to call extract_weather tool for biratnagar as input for city"}
#     PLAN : {"step" : "TOOL" ,"tool":"extract_weather" "input":"biratnagar"}
#     PLAN : {"step" : "OBSERVE" ,"tool":'extract_weather', "output":"The weather for biratnagar is Clear +26°C"}
#     PLAN : {"step" : "PLAN" , "Great I got the weather info about biratnagar using the tool extract_weather"}
#     OUTPUT : {"step" : "OUTPUT" , "content":"The current weather in biratnagar is 26 degree Celcius with clear sky"}

# """


# # print(response.choices[0].message.content)


# def extract_weather(city: str):
#     res = requests.get(f"https://wttr.in/{city.lower()}?format=%C+%t")
#     res.encoding = "utf-8"
#     if res.status_code == 200:
#         return f"The weather for {city.lower()} is {res.text}"
#     else:
#         return "Something wen't wrong while calling the tool"


# tool_list = {"extract_weather": extract_weather}


# def execute_tool(tool_name, tool_input):
#     return tool_list[tool_name](tool_input)


# user_input = input("> ")
# messages: List = [
#     {
#         "role": "system",
#         "content": SYSTEM_PROMPT,
#     },
#     {
#         "role": "user",
#         "content": user_input,
#     },
# ]


# while True:
#     response = client.chat.completions.create(
#         model="gpt-4o", response_format={"type": "json_object"}, messages=messages
#     )

#     result = json.loads(response.choices[0].message.content)
#     print(f"🤖 : {result}")
#     messages.append({"role": "assistant", "content": json.dumps(result)})
#     if result["step"] == "TOOL":
#         # Execute the tool
#         tool_output = execute_tool(result["tool"], result["input"])
#         # Inject as OBSERVE
#         observe = {"step": "OBSERVE", "output": tool_output}
#         messages.append({"role": "user", "content": json.dumps(observe)})

#     elif result["step"] == "OUTPUT":
#         print("Final Answer:", result["content"])
#         break
