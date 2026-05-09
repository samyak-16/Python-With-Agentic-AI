from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()


code_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI code generator."),
        ("human", "{topic}"),
    ]
)

explain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI code explainer who explains the given code in simple terms.",
        ),
        ("human", "Explain the following code :\n {code}"),
    ]
)


model = ChatOpenAI(model="gpt-4o")


parser = StrOutputParser()


runnable_generate_code = code_prompt | model | parser
runnable_explain_code = explain_prompt | model | parser


runnable_paralle = RunnableParallel(
    {"code": RunnablePassthrough(), "explaination": runnable_explain_code}
)

main_runnable_chain = runnable_generate_code | runnable_paralle
response = main_runnable_chain.invoke({"topic": "Python Code to  find SI"})
print()
print()
print()
print()
print(response["code"])
print()
print()
print()
print()
print(response["explaination"])
print()
print()
print()
print()
