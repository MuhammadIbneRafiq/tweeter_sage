import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from groq import Groq
from langchain_groq import ChatGroq
from datetime import datetime
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from typing import Union, List, Tuple, Dict
from langchain.schema import Document
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

# Load environment variables
load_dotenv()

# Set up Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# Set up HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load and process the HTML file
url = './ui_ux_designer_expanded.html'
loader = UnstructuredHTMLLoader(url)
documents = loader.load()

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=600)
splits = text_splitter.split_documents(documents)

# Create and persist the vector store
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
vectorstore.persist()

# Create a retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
print('mem', memory, type(memory))

# Define the system prompt
system_prompt = """You are an AI assistant specializing in freelance recruitment and job posting analysis. Your task is to help users find relevant job postings, particularly for UI/UX designers, freelance projects, and opportunities with agencies or small companies. When providing information about job postings, focus on the following details:

1. Profile link of the person or company posting (if available)
2. Brief description of the job post
3. Link to the full job post
4. Name of the person or company posting (if available)
5. Payment amount or rate (if specified)

Always prioritize active hiring posts and avoid confusing them with general hiring-related discussions. Provide concise, accurate information and be ready to answer follow-up questions about the job market, freelancing trends, and specific job opportunities.

When asked to find job postings, aim to provide at least 3 relevant results at a time, formatted in a clear and easy-to-read manner. If the user asks for more results, provide the next set of 3 job postings that haven't been mentioned before.

Remember to maintain context throughout the conversation and refer back to previously discussed information when relevant."""

def generate(query: str, docs: list[str], chat_history: list):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    # Add chat history to the messages
    messages.extend(chat_history)
    
    # Add context from retrieved documents
    context = "\n\nContext:\n" + "\n---\n".join(docs)
    messages.append({"role": "system", "content": context})
    
    # Generate response
    chat_response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    return chat_response.choices[0].message.content

# Create a ConversationalRetrievalQA chain
    # rag_prompt_chain = rag_prompt | GROQ_LLM | StrOutputParser()

# qa_chain = RunnablePassthrough(
#     retriever=retriever,
#     memory=memory,
#     llm=groq_client,
#     qa_template=generate()
# )

# Function to handle user queries
def handle_query(query: str):
    # Retrieve relevant documents
    relevant_docs = retriever.get_relevant_documents(query)
    
    # Extract the content from the relevant documents
    doc_contents = [doc.page_content for doc in relevant_docs]
    
    # Generate the response using the Groq client
    result = generate(query=query, docs=doc_contents, chat_history=[])
    
    # Update memory with the new interaction
    # memory.save_context({"role": "user", "content": query}, {"role": "assistant", "content": result})
    
    # Print the result
    print("AI: " + result)
    print("\n" + "-"*50 + "\n")

# Main loop for user interaction
print("Welcome to the Freelance Job Search Assistant!")
print("You can ask up to 10 questions about UI/UX design jobs, freelance opportunities, and more.")
print("Type 'quit' to exit the program at any time.\n")

for i in range(100):
    user_query = input(f"Question {i+1}/10: ")
    if user_query.lower() == 'quit':
        print("Thank you for using the Freelance Job Search Assistant. Goodbye!")
        break
    handle_query(user_query)

if i == 99:
    print("You've reached the maximum number of questions. Thank you for using the Freelance Job Search Assistant!")