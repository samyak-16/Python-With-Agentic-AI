from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="Test RAG",
)
user_query = input("Ask something related to the pdf :  ")

search_results = vector_store.similarity_search(
    query=user_query
)  # Returns Relevent chunks from vector db

context = "\n\n\n".join(
    [
        f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File Location : {result.metadata['source']}"
        for result in search_results
    ]
)
# print("==" * 50)
# print(type(search_results[0].model_dump()))
# print(search_results[0].model_dump()["page_content"])
# for result in search_results:
#     print(result)
#     print("==" * 50)


SYSTEM_PROMPT = f"""
You are a helpfull AI Assistant who answers user query based on the available context retrieved from a PDF File along with page_content and page_number.

You should only ans the user based on the following context and navigate the user to open the right page number to know more .

Context : {context}
# """
client = OpenAI()


response = (
    client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )
)

print(f"🤖 : {response.choices[0].message.content}")
