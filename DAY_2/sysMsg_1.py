import ollama 
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"system",
            "content":"Give the answers in 2-3 lines only."
        },
        {
            "role":"user",
            "content":"explain ddl commands"
        }
    ]
)
print(response["message"]["content"])