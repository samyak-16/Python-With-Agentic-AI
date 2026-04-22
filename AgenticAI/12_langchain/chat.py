from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(name="gpt-4o-mini")


messages = [SystemMessage("You are a funny AI Agent")]
print("--------------- Enter 0 for closing thr loop --------------------")

while True:
    query = input("USER : ")
    if query == "0":
        break
    messages.append(HumanMessage(query))
    ai_response = model.invoke(messages)  # Short term memory
    messages.append(ai_response)  # ai_response is already AIMessage type :
    print("AI : ", ai_response.content)

print("=" * 50)
[print(message.content) for message in messages]
