from google.adk.agents.llm_agent import Agent
from .tools import steam_reviews, reddit_reviews


# 1) Data Agent (has tool access)
game_data_agent = Agent(
    model="gemini-2.5-flash",
    name="game_data_agent",
    description="Fetches and structures game reviews and engagement metrics",
    tools=[steam_reviews],
    instruction="""
You fetch real review data using steam_reviews tool when a game name is given.
Return structured insights:
- overall sentiment
- key pros and cons
- engagement indicators (review volume and positivity)
Be factual and concise.
"""
)

# Reddit Data Agent
reddit_data_agent = Agent(
    model="gemini-2.5-flash",
    name="reddit_data_agent",
    description="Fetches and summarizes Reddit community feedback",
    tools=[reddit_reviews],
    instruction="""
Fetch Reddit posts using reddit_reviews for a given game.
Summarize:
- common praise points
- common complaints
- overall community sentiment
Include notable recurring themes.
Be concise.
"""
)

# Recommendation Agent (uses both data agents)
recommendation_agent = Agent(
    model="gemini-2.5-flash",
    name="recommendation_agent",
    description="Combines Steam + Reddit feedback into a recommendation",
    sub_agents=[game_data_agent, reddit_data_agent],
    instruction="""
When the user mentions a specific game:
1. Call game_data_agent to get Steam review insights.
2. Call reddit_data_agent to get Reddit community feedback.
3. Combine both to provide:
   - who this game is best for
   - who should avoid it
   - current state (worth buying/playing now?)
   - a short verdict

Be balanced and practical.
"""
)

# Root Agent (entry point for ADK Web)
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Entry point agent for game reviews and recommendations",
    sub_agents=[recommendation_agent],
    instruction="""
You are the entry point.

If a specific game is mentioned:
- Delegate to recommendation_agent.

If the user asks general gaming questions:
- Answer directly.

Always provide a clear final response.
"""
)