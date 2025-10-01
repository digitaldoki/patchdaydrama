import gradio as gr
from openai import OpenAI

# Initialize client (HF injects API key automatically)
client = OpenAI()

# --- System Prompt ---
SYSTEM_PROMPT = """
You are Lubby Llama, the Patch Day Drama AI helper.
Rules:
1. Help players troubleshoot Sims-style mod and patch issues.
2. Always suggest safe fixes (update mods, clear cache, repair game).
3. Never suggest pirated or unsafe content.
4. Be playful, supportive, and llama-themed in tone.
"""

# --- Chat function ---
def chat_fn(message, history):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history:
        role = "user" if h[0] else "assistant"
        msgs.append({"role": role, "content": h[1]})
    msgs.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=msgs,
    )
    reply = response.choices[0].message.content
    return reply

# --- CSS styling with animated glow ---
custom_css = """
body {
  background: linear-gradient(135deg, #ff66b2, #ff3399);
  font-family: 'Comic Sans MS', sans-serif;
}

#chatbot {
  border: 3px solid #00ff99 !important;
  border-radius: 20px !important;
  background: #fff8fb !important;
  animation: neon-glow 2s infinite alternate;
}

@keyframes neon-glow {
  from {
    box-shadow: 0 0 15px #00ff99, 0 0 30px #00ff99;
  }
  to {
    box-shadow: 0 0 25px #00ffcc, 0 0 50px #00ffcc;
  }
}

textarea, input {
  border: 2px solid #00ff99 !important;
  border-radius: 12px !important;
}

button {
  background: #00ff99 !important;
  color: black !important;
  font-weight: bold !important;
  border-radius: 12px !important;
}

button:hover {
  background: #00cc7a !important;
}
"""

# --- Interface layout ---
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML("<h1>🦙 Patch Day Drama — Lubby Llama to the Rescue!</h1>"
                    "<p>Patch day chaos? Mods broken? Lubby’s got your back 🦙🔧</p>")
            chatbot = gr.Chatbot(elem_id="chatbot", height=400)
            msg = gr.Textbox(placeholder="Type your message...")
            clear = gr.Button("Clear")
        with gr.Column(scale=1):
            gr.Image("assets/img/lubby.png", show_label=False)

    msg.submit(chat_fn, [msg, chatbot], chatbot)
    msg.submit(lambda: "", None, msg)  # clear input after sending
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
