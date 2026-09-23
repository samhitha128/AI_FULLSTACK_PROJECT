import ollama 
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"system",
            "content":"image you are a 7 year old child and give answers in 4 lines"
        },
        {
            "role":"user",
            "content":"explain ml"
        }
    ]
)
print(response["message"]["content"])