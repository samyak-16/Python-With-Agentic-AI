from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="Test RAG",
)


def query_handler(query: str):
    print("Serching Similar Index for this query :", query)
    search_results = vector_store.similarity_search(
        query=query
    )  # Returns Relevent chunks from vector db
    context = "\n\n\n".join(
        [
            f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File Location : {result.metadata['source']}"
            for result in search_results
        ]
    )
    SYSTEM_PROMPT = f"""
You are a helpfull AI Assistant who answers user query based on the available context retrieved from a PDF File along with page_content and page_number.

You should only ans the user based on the following context and navigate the user to open the right page number to know more .

Context : {context}
# """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    print(f"🤖 : {response.choices[0].message.content}")
    return response.choices[0].message.content
