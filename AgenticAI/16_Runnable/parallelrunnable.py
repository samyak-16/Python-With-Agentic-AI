from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()


short_prompt = ChatPromptTemplate.from_template("Explain {topic} in short and simple")

long_prompt = ChatPromptTemplate.from_template("Explain {topic} in detail")


model = ChatOpenAI(model="gpt-4o")


parser = StrOutputParser()


topic = "Machile Learning"

short_runnable = short_prompt | model | parser
long_runnable = long_prompt | model | parser

combined_runnable = RunnableParallel(
    {"short_response": short_runnable, "long_response": long_runnable}
)
results = combined_runnable.invoke({"topic": topic})
print()
print()
print()
print("Short Result : ", results["short_response"])
print()
print()
print()
print("Detailed Result : ", results["long_response"])
