import gradio as gr
from agent_runner import app
from langchain_core.messages import HumanMessage

# === Backend Function ===
def chat_with_agent(user_input, history):
    # Convert history to message list if needed
    messages = [HumanMessage(content=msg[0]) for msg in history]
    messages.append(HumanMessage(content=user_input))

    result = app.invoke({"messages": messages})
    reply = result["messages"][-1].content
    history.append((user_input, reply))
    return "", history

# === UI Setup ===
with gr.Blocks(title="Elderly Care AI Assistant") as demo:
    gr.Markdown("## 🧓🤖 Elderly Care AI Assistant\nAsk me anything related to health, safety, reminders, or medicine!")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask your elderly care assistant...")
    clear = gr.Button("Clear")

    history_state = gr.State([])

    msg.submit(chat_with_agent, [msg, history_state], [msg, chatbot])
    clear.click(lambda: ([], ""), None, [chatbot, msg, history_state])

# === Launch ===
if __name__ == "__main__":
    demo.launch()
