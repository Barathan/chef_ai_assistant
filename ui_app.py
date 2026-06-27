import os
import streamlit as st  # Clean and correct!
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. Page Configuration (Sets title and professional layout)
st.set_page_config(page_title="Chef AI - Michelin-Star Recipes", page_icon="🍳", layout="centered")

# Custom Colorful Header
# Custom Colorful Header
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍳 Chef AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777777;'>Your personal Michelin-star chef. Ask for recipes, ingredient swaps, or culinary advice!</p>", unsafe_allow_html=True)
st.write("---")

# 2. Securely Setup OpenAI API Key (Replace with yours)
os.environ["OPENAI_API_KEY"] = "your-actual-api-key-here"

# 3. Initialize the LangChain LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 4. Define the Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a professional Michelin-star chef. Give creative, elegant, yet easy-to-follow recipe advice."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])
chain = prompt_template | llm

# 5. Initialize Chat History in Streamlit Session State (This keeps memory alive!)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 6. Display Past Conversation on Screen
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="👨‍🍳"):
            st.write(message.content)

# 7. Accept User Input
if user_query := st.chat_input("Type your ingredient or question here (e.g., 'What can I make with potatoes?')..."):
    
    # Display user's message instantly
    with st.chat_message("user"):
        st.write(user_query)
        
    # Append user message to memory state
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    # Generate response with Streaming in the UI
    with st.chat_message("assistant", avatar="👨‍🍳"):
        # st.write_stream reads a generator and animates text automatically!
        def stream_response():
            for chunk in chain.stream({"input": user_query, "chat_history": st.session_state.chat_history}):
                yield chunk.content

        full_response = st.write_stream(stream_response)
        
    # Append assistant's response to memory state
    st.session_state.chat_history.append(AIMessage(content=full_response))