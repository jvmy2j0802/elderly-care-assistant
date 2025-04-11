from transformers import pipeline
from langchain_huggingface import ChatHuggingFace
from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated

# === Local Tools ===
from tools.health_tools import get_recent_health_alerts
from tools.db_tools import get_user_info, med_info
from tools.safety_tools import get_recent_falls

# === LLM Setup ===
model_id = "google/flan-t5-small"
hf_pipeline = pipeline(
    "text2text-generation",
    model=model_id,
    tokenizer=model_id,
    max_length=512,
    do_sample=True,
)
llm = ChatHuggingFace(pipeline=hf_pipeline)

# === State Definition ===
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "Messages"]

# === Default LLM Agent ===
def ai_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state

# === Routing Logic ===
def route_tool(state: AgentState):
    user_input = state["messages"][-1].content.lower()
    if any(term in user_input for term in ["health", "heart", "glucose", "spo2", "oxygen", "alerts"]):
        return "health_alerts"
    elif any(term in user_input for term in ["fall", "incident", "safety"]):
        return "fall_events"
    elif any(term in user_input for term in ["user info", "user profile", "who is", "about user"]):
        return "user_info"
    elif any(term in user_input for term in ["medicine", "medication", "drugs", "tablet"]):
        return "medicine_info"
    else:
        return "ai_agent"

# === LangGraph Workflow ===
workflow = StateGraph(AgentState)

# Agent & Tools
workflow.add_node("ai_agent", ai_agent)
workflow.add_node("health_alerts", get_recent_health_alerts)
workflow.add_node("fall_events", get_recent_falls)
workflow.add_node("user_info", get_user_info)
workflow.add_node("medicine_info", med_info)

# Entry Point
workflow.set_entry_point("ai_agent")

# Conditional Routing
workflow.add_conditional_edges("ai_agent", route_tool, {
    "health_alerts": "health_alerts",
    "fall_events": "fall_events",
    "user_info": "user_info",
    "medicine_info": "medicine_info",
    "ai_agent": END,
})

# End Nodes
workflow.add_edge("health_alerts", END)
workflow.add_edge("fall_events", END)
workflow.add_edge("user_info", END)
workflow.add_edge("medicine_info", END)

# Compile app
app = workflow.compile()
