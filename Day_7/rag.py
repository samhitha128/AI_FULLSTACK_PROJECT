from sentence_transformers import SentenceTransformer
import chromadb,ollama,streamlit as st
#model= SentenceTransformer("all-MiniLM-L6-v2")
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
model=load_model()
st.title(":red[TALK WITH SAMMY!! 🤖]")
if "messages" not in st.session_state:
    st.session_state.messages=[]
with st.sidebar:
    st.header(":blue[Chat Settings ⚙️]")
    personalities={
            "Kid👶🏻":"Give the answers like you are explaining to a 5 year old kid.Give the answer in 2 lines only,",
            "Professor👩🏻‍🏫":"You are an IIT professor.Explain the topics using correct teminology.Give the answer in 2-3 lines only",
        }
    personality=st.selectbox(":grey[Select a personality]",personalities.keys())
    top_k=st.slider("Select no of top results",min_value=1,max_value=5,value=3)
    
    
    uploaded_file=st.file_uploader("Upload a file")
    if uploaded_file:
        st.success("*File uploaded successfully✅*")
        text=uploaded_file.read().decode("utf-8")
        with st.expander("Preview👇🏻"):
            st.text(text)
    
    
#file_name="sample.txt"
#with open(file_name,"r") as file:
    #text=file.read()
#chunking
        chunks=[]
        chunk_size=100
        chunk_overlap=20
        step=chunk_size-chunk_overlap #100-20=80
        for i in range(0,len(text),step):
            chunk=text[i:i+chunk_size] #(0-100)(80-180)(160-260)
            chunks.append(chunk)
        #for i in range(len(chunks)):
            #print(f"Chunk{i+1} -> {chunks[i]}")

        #embedding
        embeddings = model.encode(chunks)
        #print(embeddings[0])
        #print(len(embeddings))
        #print(embeddings.shape)

        #Vector DB
        client=chromadb.PersistentClient(path="./chroma_db")
        collection= client.get_or_create_collection(name="My_Documents")
        ids=[]
        for i in range(len(chunks)):
            ids.append(f"{uploaded_file.name}_{i}")
        collection.add(
            documents=chunks,
            ids=ids,
            embeddings=embeddings.tolist()
        )
    st.subheader("Chat options")
    with st.container():
        if st.button("Clear Chat 🗑️"):
            st.session_state.messages=[]
            st.success("*chat cleared successfully✅*")
    with st.expander("Chat History"):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    
#results=collection.get()
#chunk1=collection.get(ids=['sample.txt_0'])
#print(chunk1)

#Query Phase
question=st.chat_input("Ask a question:👀")
if question:
    if uploaded_file:
        st.write(question)
        q_embedding = model.encode(question)
        #top_k=3
        results=collection.query(
            query_embeddings=[q_embedding.tolist()],
            n_results=top_k
        )
        retrieved_chunks=(results['documents'][0])
        retrieved_ids=results["ids"][0]
        #print(retrieved_chunks)
        #for i in range(len(results['documents'][0])):
        #   print(f"Chunk{i+1}")
        #   print(results['documents'][0][i])
        context='\n'.join(retrieved_chunks)
        #print(context)

        #prompt
        prompt = f'''
        Answer the question using the context given below only. 
        Question:{question}
        Context:{context}
        Answer:
        '''
        #print(prompt)
        response=ollama.chat(
            model="llama3.2:3b",
            messages=[{"role":"user","content":prompt}]
        )
        st.write(response["message"]["content"])
    else:
        with st.chat_message("user"):
            st.write("User:",question)
        st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )
        with st.spinner(":grey[Think while we are proccessing 😉]"):
            response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role":"system","content":personalities[personality]
                            }
                        ]+ st.session_state.messages
                    )
        st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response["message"]["content"]
                    }
                )
        with st.chat_message("assistant"):
            st.write("AI:", response["message"]["content"])
        
       