# File: research_agent.py
from autogen import AssistantAgent, UserProxyAgent, register_function
from paper_search_tool import search_papers
from config import LLM_CONFIG

assistant = AssistantAgent(
    name="ResearchAssistant",
    llm_config=LLM_CONFIG
)

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config=False
)

register_function(
    search_papers,
    caller=assistant,
    executor=user_proxy,
    name="search_papers",
    description=(
        "You are a helpful AI research assistant. Your job is to find research papers based on a given prompt.\n"
        "Always use the `search_papers` tool for literature queries.\n\n"
        "Function arguments:\n"
        "- topic (str): Required. Topic to search for.\n"
        "- year (int): Required. Publication year filter.\n"
        "- comparator (str): Optional. One of 'in', 'before', or 'after' (e.g., 'after' 2000).\n"
        "- min_citations (int): Optional. Minimum number of citations.\n"
        "- author, keywords: Optional filters.\n\n"
        "Function return:\n"
        "- List of dicts with: title, authors, year, citations, url.\n"
        "- Return an empty list with an explanation if no results.\n"
        "- Return an error message if the call fails.\n\n"
        "Do NOT output Python code. Always return results through the tool call."
    )
)

user_proxy.initiate_chat(
    assistant,
    message="Find research papers on ADHD, published after 2000 with at least 10 citations."
)
