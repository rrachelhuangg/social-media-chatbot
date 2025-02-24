import chainlit as cl
import asyncio
from langchain.memory.buffer import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from prompts import social_media_assistant_prompt_template
from dotenv import load_dotenv
from extract_data import download_general
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain import hub

#setting environment variables
load_dotenv()

#setting up qdrant vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

client = QdrantClient(url="http://localhost:6333")
if not client.collection_exists("initial-collection"):
    client.create_collection(
        collection_name="initial-collection",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
vector_store = QdrantVectorStore(
    client=client,
    collection_name="initial-collection",
    embedding=embeddings,
)

@cl.on_chat_start
async def query_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0.7)
    rag_prompt = hub.pull('rlm/rag-prompt')
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   input_key="question",
                                                   max_len=50,
                                                   return_messages = True)
    llm_chain = LLMChain(llm=llm, prompt = rag_prompt, memory=conversation_memory)
    cl.user_session.set("llm_chain", llm_chain)
    await cl.Message("hello! i'm stark, your social media analysis chatbot.").send()
    response = await cl.AskUserMessage(content = "what's your instagram username?", timeout = 120).send()
    user_name = ""
    if response is not None:
        username = await (download_general(response['output']))
        text = f"thank you {user_name}. your data has been downloaded successfully."
        loader = TextLoader("followed.txt")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            add_start_index = True,
        )
        all_splits = text_splitter.split_documents(docs)

        document_ids = vector_store.add_documents(documents=all_splits)
        await cl.Message(text).send()

@cl.on_message 
async def query_llm(message: cl.Message):
    question = message.content
    retrieved_docs = vector_store.similarity_search(question)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    llm_chain = cl.user_session.get("llm_chain")
    response = await llm_chain.acall({"question": question, "context": docs_content}, callbacks = [cl.AsyncLangchainCallbackHandler()])
    await cl.Message(response["text"]).send()

if __name__ == '__main__':
    query_llm("What's my name?")