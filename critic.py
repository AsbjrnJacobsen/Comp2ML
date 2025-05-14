# File: critic.py

import time
import logging
import autogen
from config import LLM_CONFIG
from research_agent import assistant as research_agent
from paper_search_tool import search_papers

logging.basicConfig(level=logging.INFO)

critic_agent = autogen.AssistantAgent(name="critic_agent", llm_config=LLM_CONFIG)

prompts = [
    "Find research papers on ADHD, published after 2000 with at least 10 citations.",
    "Find research on weight loss, published after 2000 with at least 10 citations.",
    "Find research on nutritional therapy, published after 2010 with at least 10 citations.",
    "Find papers on Carnivore Diet (Only eating animal products), published after 2010 with at least 10 citations.",
    "Find papers on why chicken nuggets are good for you."
]

for prompt in prompts:
    chat = [{"role": "user", "content": prompt}]
    time.sleep(1)

    try:
        reply = research_agent.generate_reply(chat)
        content = reply.get("content", "")
        tool_calls = reply.get("tool_calls", [])
    except Exception as e:
        content = f"[ERROR: {e}]"
        tool_calls = []

    chat.append({"role": "assistant", "content": content})

    if tool_calls:
        for tool in tool_calls:
            args = eval(tool["function"]["arguments"])  # trust inputs now
            result = search_papers(**args)
            response = str(result)
            chat.append({
                "role": "tool",
                "tool_call_id": tool["id"],
                "name": tool["function"]["name"],
                "content": response
            })
            chat.append({"role": "assistant", "content": response})
            break

    eval_prompt = f"""
    Strictly return a JSON object with the following keys exactly:
    "Relevance", "Accuracy", "Consistency", "Comprehensiveness", "Completeness", "Additional Information", "Feedback".

    - Each value should be a number (1–5) or a short string.
    - "Feedback" must contain your own evaluation of the assistant's response.
    - No markdown, no formatting — return only a valid JSON object.

    User Prompt: {prompt}
    Agent Response: {chat[-1]["content"]}
    """.strip()

    time.sleep(1)
    critic_reply = critic_agent.generate_reply([{"role": "user", "content": eval_prompt}])
    critic_content = critic_reply.get("content", "")

    print(f"\n{'='*80}")
    print(f"PROMPT: {prompt}\n")
    print(f"AGENT RESPONSE:\n{chat[-1]['content']}\n")
    print(f"CRITIC FEEDBACK:\n{critic_content}")
    print(f"{'='*80}\n")
