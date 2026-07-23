from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient


class Source(BaseModel):
    """Schema for a source used by the agent"""

    url:str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer:str = Field(description="The Agents answer to the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the response")



tavily = TavilyClient()


def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: The query to search for
    Returns: 
        The search result
    """
    print(f"Searching for query {query}")
    return tavily.search(query=query)

llm = ChatOpenAI()
tools = [search]
agent=create_agent(model=llm, tools=tools, response_format=AgentResponse)

def main():
    print("Hello from langchain-course")
    result = agent.invoke({"messages":HumanMessage(content="Search for AI engineer jobs using Langchain in Toronto ,  Ontario area on Linkedin and list their details ")})
    print(result)
if __name__ == "__main__":
    main()
