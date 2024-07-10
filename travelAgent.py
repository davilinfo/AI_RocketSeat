import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, create_react_agent, AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub, text_splitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import bs4

llm = ChatOpenAI(model='gpt-3.5-turbo')
query = """
Vou viajar para Londres em Agosto de 2024. 
Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço de passagem de São Paulo para Londres
"""

def researchAgent(query, llm):    
    tools = load_tools(['ddg-search', 'wikipedia'], llm=llm)
    #print(tools[0].name, tools[0].description)
    #print(tools[1].name, tools[1].description)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent,tools=tools,prompt=prompt, verbose=True)
    webContext = executor.invoke({"input":query})
    
    return webContext['output']

    #deprecated in 0.3.0
    #agent = initialize_agent(
    #    tools,
    #    llm,
    #    agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #    verbose=True,
        # memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
    #)
    #depreacted in 0.3.0
    #print (agent.agent.llm_chain.prompt.template)
    #deprecatedin 0.3.0 of initialize_agent
    #agent.run(query)

def loadData():
    loader = WebBaseLoader(
        web_paths=('https://www.dicasdeviagem.com/inglaterra/'),
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=('postcontentwrap','pagetitleloading background-imaged loading-dark')))
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)#loads page on each 1000 token(near to a word)
    splits = text_splitter.split_documents(docs)
    vectorstore=Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings)
    retriever = vectorstore.as_retriever()
    return retriever

def getRelevantDocs(query):
    retriever = loadData()
    relevant_documents = retriever.invoke(query)
    print (relevant_documents)
    return relevant_documents

def supervisorAgent(query,llm,webContext,relevant_documents):
    prompt_template = """
    você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagem completo e detalhado.
    Utilize o context de evento e preço de passagens, o input do usuário e também os documentos relevantes para elaborar o roteiro.
    Contexto: {webContext}
    Document relevante: {relevant_documents}
    Usuário: {query}
    Assistente:
    """
    prompt = PromptTemplate(
        input_variables=['webContext','relevant_documents','query'],
        template=prompt_template
    )

    sequence = RunnableSequence(prompt | llm)

    response = sequence.invoke({"webContext": webContext, "relevant_documents":relevant_documents, "query":query})
    return response

def getResponse(query, llm):
    webContext = researchAgent(query=query, llm=llm)
    relevant_documents = getRelevantDocs(query=query)
    response = supervisorAgent(query=query,llm=llm,webContext=webContext,relevant_documents=relevant_documents)
    return response

print(getResponse(query=query, llm=llm).content)