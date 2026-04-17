# This file helps for indexing the data into the vector db ->(Run this file one time only)
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "ai_roadmap.pdf"


loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()
# print(len(docs))  # 13 (one per page)
# print(docs[0])  # Document(page_content='...', metadata={...})
# print(docs[0].page_content)  # the raw text of page 1
# print(docs[0].metadata)  # {'source': 'file.pdf', 'page': 0}

# Split the docs into smaller chunks

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents=docs)
print(f"Docs further Broken into {len(chunks)} chunks")
# for chunk in chunks:
#     print(chunk.page_content)
#     print("==" * 50)

# Now embeddings the chunks to vector db
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)

# vector_store = QdrantVectorStore()  # just connects to an existing Qdrant collection. Does not embed or store anything. You'd use this when your data is already indexed and you just want to query it.
print("Indexing document started ..")
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="Test RAG",
)  # connects + embeds all your chunks + stores them into Qdrant in one call.
