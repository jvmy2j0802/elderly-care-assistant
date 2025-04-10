import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gradio as gr
from agent_runner import app

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask your elderly care assistant:")
    clear = gr.Button("Clear")

    def user(message, history):
        history = history or []
        history.append((message, ""))
        return "", history

    def bot(history):
        user_input = history[-1][0]
        response_stream = app(user_input)
        final_response = ""
        for partial_response in response_stream:
            final_response += partial_response
            history[-1] = (user_input, final_response)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
