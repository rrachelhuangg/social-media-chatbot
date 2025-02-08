import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from prompts import social_media_assistant_prompt_template
from dotenv import load_dotenv

#setting environment variables
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125",
             temperature = 0.7)

llm_chain = LLMChain(llm=llm, prompt = social_media_assistant_prompt_template)

def query_llm(question):
    print(llm_chain.invoke({'question': question})['text'])

if __name__ == '__main__':
    query_llm("What's my name?")