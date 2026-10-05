from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext
import threading
import os

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are Thaif AI Assistant. Always respond in English unless the user explicitly asks for another language. Give clear, helpful answers in simple language."
    }
]


def send_message():
    question = entry.get().strip()

    if not question:
        return

    chat.insert(tk.END, "You: " + question + "\n\n")
    entry.delete(0, tk.END)

    messages.append({
        "role": "user",
        "content": question
    })

    send_button.config(state=tk.DISABLED)
    status_label.config(text="AI is thinking...")

    threading.Thread(
        target=get_ai_response,
        daemon=True
    ).start()


def get_ai_response():
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )

        answer = response.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": answer
        })

        root.after(0, show_response, answer)

    except Exception as e:
        root.after(0, show_response, "Error: " + str(e))


def show_response(answer):
    chat.insert(tk.END, "AI: " + answer + "\n\n")
    chat.see(tk.END)

    send_button.config(state=tk.NORMAL)
    status_label.config(text="Ready")


root = tk.Tk()
root.title("Thaif AI Assistant")
root.geometry("750x600")

title = tk.Label(
    root,
    text="Thaif AI Assistant",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

chat = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 11)
)
chat.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

bottom_frame = tk.Frame(root)
bottom_frame.pack(
    fill=tk.X,
    padx=10,
    pady=10
)

entry = tk.Entry(
    bottom_frame,
    font=("Arial", 12)
)
entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    padx=(0, 10)
)

send_button = tk.Button(
    bottom_frame,
    text="Send",
    command=send_message,
    font=("Arial", 11, "bold")
)
send_button.pack(side=tk.RIGHT)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 9)
)
status_label.pack(pady=5)

entry.bind(
    "<Return>",
    lambda event: send_message()
)

root.mainloop()