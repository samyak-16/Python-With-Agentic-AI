from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# 1) Prompt Template
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple words")

# 2) Model

model = ChatOpenAI(model="gpt-4o")

# 3) Output Parser

parser = StrOutputParser()

#! Step-by-step manual flow

# #  Format the prompt

# formatted_prompt = prompt.format_prompt(topic="Machine Lerarning")

# # Call the model manually

# response = model.invoke(formatted_prompt)

# # Parse the resopnse

# parsed_response = parser.invoke(response)


# print("Final output : ", parsed_response)

#!  flow using runnable

runnable = prompt | model | parser
result = runnable.invoke({"topic": "Explain LLM in simple terms for a beginner"})
