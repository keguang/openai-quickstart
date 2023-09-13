import gradio as gr
import openai


def reset(input):
    return []


# Function that powers the chatbot by sending and receiving messages from OpenAI
def sales_chat(message, history, sale_type_name):

    chat_history = [{"role": "system", "content": f"你是一个资深的{sale_type_name}销售"}]

    for human, assistant in history:
        chat_history.append({"role": "user", "content": human})
        chat_history.append({"role": "assistant", "content": assistant})

    if message:
        # Continue chat sequence and append AI's response
        chat_history.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=chat_history
        )  # Get response from OpenAI model
        reply = chat.choices[0].message.content

        return reply


# Gradio app
chatbot = gr.Chatbot(height=300)
with gr.Blocks() as demo:
    gr.Markdown("智能客服")
    dropdown = gr.Dropdown(
        ["电器", "家装", "教育"], label="请选择一个销售类型", info="请下拉选择一个销售来对话", value="电器"
    )

    chat = gr.ChatInterface(fn=sales_chat, chatbot=chatbot, additional_inputs=dropdown)

    # 在下拉菜单值更改时，设置当前销售类型的历史对话
    dropdown.input(fn=reset, inputs=dropdown, outputs=chatbot)
    dropdown.input(
        fn=reset,
        inputs=dropdown,
        outputs=None,
    )

demo.queue()
demo.launch(share=True, server_name="0.0.0.0")
