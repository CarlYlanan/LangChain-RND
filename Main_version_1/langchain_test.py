from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature=0.7,
    max_completion_tokens=1000,
    verbose=True
    )

response = llm.batch(["What are you?","Do you appreciate the current educative state?"] )
for response in response:
    print(response.content)
    print("\n---\n")

    
