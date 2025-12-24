""" A core agent implementation for managing AI interactions. """

from langchain_groq import ChatGroq
from langchain_tavily.tavily_search import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from src.config.settings import settings

def get_response_from_ai_agents(llm_id , query , allow_search ,system_prompt):
    """Get response from AI agents based on the provided parameters."""
    if llm_id not in settings.ALLOWED_MODELS_NAMES:
        raise ValueError(f"Model {llm_id} is not allowed.")
    
    llm = ChatGroq(model_name=llm_id, api_key=settings.GROQ_API_KEY)
    
    tools = [TavilySearch(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )

    state = {"messages" : query}
    response = agent.invoke(state)
    messages = response.get("messages")

    response = [message.content for message in messages if isinstance(message,AIMessage)]

    return response[-1]