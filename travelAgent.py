import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, create_react_agent, AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub

llm = ChatOpenAI(model='gpt-3.5-turbo')

tools = load_tools(['ddg-search', 'wikipedia'], llm=llm)

#print(tools[0].name, tools[0].description)
#print(tools[1].name, tools[1].description)

#prompt = hub.pull("hwchase17/react")

#agent = create_react_agent(llm=llm,tools=tools, prompt=prompt)

#executor = AgentExecutor(agent=agent,tools=tools,prompt=prompt, verbose=True)

#deprecated in 0.3.0
agent = initialize_agent(
    tools,
    llm,
    agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    # memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
)

#depreacted in 0.3.0
print (agent.agent.llm_chain.prompt.template)

query = """
Vou viajar para Londres em Agosto de 2024. 
Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço de passagem de São Paulo para Londres
"""
#deprecatedin 0.3.0 of initialize_agent
agent.run(query)

#executor.invoke({"input":query})