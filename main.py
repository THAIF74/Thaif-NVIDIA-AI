from openai import OpenAI
from dotenv import load_dotenv
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

print("\n🤖 Thaif AI Assistant")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("AI: Goodbye bro! 👋")
        break

    messages.append({
        "role": "user",
        "content": question
    })

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

    print("\nAI:", answer)
    print()