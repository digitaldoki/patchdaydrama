import gradio as gr
from openai import OpenAI

# Initialize client (Hugging Face injects your API key automatically)
client = OpenAI()

# --- Lubby Llama System Prompt ---
SYSTEM_PROMPT = """
You are Lubby Llama, the Patch Day Drama AI helper.
Rules:
1. Help players troubleshoot Sims-style mod and patch issues.
2. Always suggest safe fixes (update mods, clear cache, repair game).
3. Never suggest pirated or unsafe content.
4. Be playful, supportive, and llama-themed in tone.
"""

# --- Chat logic ---
def chat_with_lubby(message, history):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- UI ---
with gr.Blocks(css="assets/custom.css") as demo:
    gr.Markdown("## 🦙 Patch Day Drama — Lubby Llama to the Rescue!")
    gr.ChatInterface(fn=chat_with_lubby, type="messages")

if __name__ == "__main__":
    demo.launch()

