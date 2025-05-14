## What to do:

Install the dependencies from requirements.txt
````pip install -r requirements.txt```` 

Create a .env file and set your API key(mistral). 

run research_agent.py or critic.py to get the agents running.
```python research_agent.py```
```python critic.py```
If you run critic, you will first run research agent.
You need to hit enter and/or typ exit to advance/stop the chat.
Once you do, the critic agent starts running with hardcoded prompts.
The prompts can be changed in the .py files for these agents.

I recommend:
run critic.py
Let it send out one response.
type: "exit" - hit enter
Look at the critic ouput.
