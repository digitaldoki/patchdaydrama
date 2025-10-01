import os
import gradio as gr
from openai import OpenAI

# --- Lubby Llama Prompt ---
SYSTEM_PROMPT = """
You are Lubby Llama, the Patch Day Drama AI helper.
Rules:
1. Help players troubleshoot Sims-style mod and patch issues.
2. Always suggest safe fixes (update mods, clear cache, repair game).
3. Never suggest pirated or unsafe content.
4. Be playful, supportive, and llama-themed in tone.
"""

# --- Initialize OpenAI client ---
client = OpenAI()  # Hugging Face handles OPENAI_API_KEY for you

# --- Free message limiter ---
MAX_FREE_MESSAGES = 5
user_messages = {}

def chat_with_lubby(message, history, username="guest"):
    """Main chat function for Lubby Llama"""
    count = user_messages.get(username, 0)
    if count >= MAX_FREE_MESSAGES:
        return (
            "🦙 You've hit the free chat limit.\n\n"
            "Support Patch Day Drama 👉 https://www.buymeacoffee.com/patchdaydrama"
        )

    user_messages[username] = count + 1

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # efficient & cheap model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# --- Build custom UI ---
with gr.Blocks(
    css="""
    body {
        background: linear-gradient(135deg, #FF1493, #FFC0CB);
        font-family: 'Trebuchet MS', sans-serif;
    }
    #chat-card {
        background: #fff8fb;
        border: 3px solid #00FF00;
        border-radius: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        padding: 20px;
        max-width: 700px;
        margin: auto;
    }
    #lubby-logo {
        max-height: 120px;
        margin-bottom: 15px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    #theme-toggle {
        margin: 10px 0;
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    #theme-toggle label {
        padding: 6px 16px;
        border-radius: 20px;
        background: #eee;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    #theme-toggle input[type=radio] { display: none; }
    #theme-toggle input[type=radio]:checked + label {
        background: #FF1493;
        color: white;
        box-shadow: 0 0 10px rgba(255,20,147,0.6);
    }
    .gradio-container { background: transparent !important; }
    footer {display:none !important;}
    """,
) as demo:

    with gr.Column(elem_id="chat-card"):
        gr.Image("./assets/img/lubby.png", elem_id="lubby-logo", show_label=False)

        with gr.Row(elem_id="theme-toggle"):
            gr.Radio(
                ["🌸 Hot Pink", "☁️ Light"],
                value="🌸 Hot Pink",
                label="",
                interactive=True,
            )

        gr.Markdown("## 💬 Ask Lubby the Llama")
        chatbot = gr.ChatInterface(fn=chat_with_lubby)


# --- Launch ---
if __name__ == "__main__":
    demo.launch()
