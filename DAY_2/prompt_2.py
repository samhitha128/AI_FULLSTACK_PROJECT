import ollama 
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"user",
            "content":"explain defination of AI in two lines and three main types of AI in bullet points "
        }
    ]
)
print(response["message"]["content"])