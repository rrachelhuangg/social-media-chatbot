import chainlit as cl
import asyncio
from langchain.memory.buffer import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from prompts import social_media_assistant_prompt_template
from dotenv import load_dotenv
from extract_data import download_general

#setting environment variables
load_dotenv()

@cl.on_chat_start
async def query_llm():
    await cl.Message("hello! i'm stark, your social media analysis chatbot.").send()
    response = await cl.AskUserMessage(content = "what's your instagram username?", timeout = 120).send()
    user_name = ""
    if response is not None:
        username = await (download_general(response['output']))
        text = f"thank you {user_name}. your data has been downloaded successfully."
        await cl.Message(text).send()
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0.7)
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=50,
                                                   return_messages = True)
    llm_chain = LLMChain(llm=llm, prompt = social_media_assistant_prompt_template)
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message 
async def query_llm(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain") #object holds the state and config needed to interact with the llm
    response = await llm_chain.acall(message.content, callbacks = [cl.AsyncLangchainCallbackHandler()])
    await cl.Message(response["text"]).send()

if __name__ == '__main__':
    query_llm("What's my name?")