from typing import TypedDict, Annotated
import operator
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_ollama import ChatOllama

# Project-specific imports
from tools import (
    get_today_reminders,
    get_recent_health_alerts,
    med_info,
    get_recent_falls,
    health_advice_retriever,
    scrape_latest_health_tips
)
from db_utils import initialize_db

# =========================
# ✅ Initialization
# =========================

# Initialize SQLite DB (creates tables if not present)
initialize_db()

# Load local Ollama model
llm = ChatOllama(model="llama3.2")

# Register all custom tools
tools = [
    med_info,
    get_today_reminders,
    get_recent_health_alerts,
    get_recent_falls,
    health_advice_retriever,
    scrape_latest_health_tips
]

# =========================
# ✅ Agent & Graph Definition
# =========================

# Agent node using LangChain ReAct + tools + Ollama
agent_node = create_react_agent(llm, tools)

# Define the LangGraph state
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

# Build LangGraph workflow
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.set_finish_point("agent")

# Compile graph into app
app = graph.compile()

# =========================
# ✅ Reusable Query Function
# =========================

def run_query(user_input: str) -> str:
    """
    Streams output from the compiled LangGraph app for a given user input.

    Args:
        user_input (str): The question or command from the user.

    Returns:
        str: The response from the AI agent.
    """
    messages = [HumanMessage(content="What are today's medication reminders?")]
    output_text = ""

    for output in app.stream({"messages": messages}):
        for _, value in output.items():
            if hasattr(value, "content") and value.content:
                output_text += value.content

    return output_text

# =========================
# ✅ Manual Test Execution
# =========================

if __name__ == "__main__":
    test_query = {
        "messages": [
            HumanMessage(content="Check if my latest health data has any anomalies and give me some health tips.")
        ]
    }

    print("User:", test_query["messages"][0].content)
    print("\nAgent Response:")

    for output in app.stream(test_query):
        print("Raw Output:", output)  # 👈 Add this to see what the agent returns
        for key, value in output.items():
            if hasattr(value, "content"):
                print(f"{key}: {value.content}")
            else:
                print(f"{key}: {value}")

