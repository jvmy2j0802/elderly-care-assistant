# LLMs & Agents
from langchain.agents import Tool
from langchain_community.chat_models import ChatHuggingFace
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END

# Transformers for Hugging Face integration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.chat_models import ChatHuggingFace

# Modular tools
from tools.health_tools import get_recent_health_alerts
from tools.safety_tools import get_recent_falls
from tools.reminder_tools import get_today_reminders

# ---------------------
# 1. Define available tools for the agent
# ---------------------
tools = [
    Tool(
        name="GetRecentHealthAlerts",
        func=get_recent_health_alerts,
        description="Fetch recent health alerts for a user. Input: user ID (string)."
    ),
    Tool(
        name="GetRecentFalls",
        func=get_recent_falls,
        description="Fetch recent fall incidents for a user. Input: user ID (string)."
    ),
    Tool(
        name="GetTodayReminders",
        func=get_today_reminders,
        description="Get today's reminders for a user. Input: user ID (string)."
    ),
]

# ---------------------
# 2. Load Hugging Face LLM
# ---------------------
model_id = "google/flan-t5-base"  # Or try "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

hf_pipeline = pipeline(
    "text2text-generation",  # Note: flan-t5 uses this task
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
)

llm = ChatHuggingFace(pipeline=hf_pipeline)

# ---------------------
# 3. Create ReAct agent using LangGraph prebuilt
# ---------------------
agent_node = create_react_agent(llm, tools)

# ---------------------
# 4. Build LangGraph stateful agent workflow
# ---------------------
builder = StateGraph()
builder.add_node("agent", agent_node)
builder.set_entry_point("agent")
builder.add_edge("agent", END)

# ---------------------
# 5. Compile the graph into an executable app
# ---------------------
app = builder.compile()

# ---------------------
# 6. Stream-compatible wrapper function for UI
# ---------------------
def app(user_input: str):
    events = app.stream({"messages": [{"role": "user", "content": user_input}]})
    full_response = ""
    for event in events:
        if "messages" in event:
            for msg in event["messages"]:
                if msg.get("role") == "assistant":
                    full_response += msg.get("content", "")
                    yield msg.get("content", "")
