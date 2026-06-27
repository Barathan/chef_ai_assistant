import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Setup API Key
os.environ["OPENAI_API_KEY"] = "your-actual-api-key-here"

# 2. Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Create a Prompt with a Placeholder for Conversation History
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a professional Michelin-star chef. Help the user with recipes and cooking advice."),
    MessagesPlaceholder(variable_name="chat_history"), # This is where memory is injected
    ("user", "{input}")
])

# 4. Create the Base Chain
chain = prompt_template | llm

# 5. Create a dictionary to store memory sessions
chats_by_session_id = {}

def get_chat_history(session_id: str):
    if session_id not in chats_by_session_id:
        chats_by_session_id[session_id] = InMemoryChatMessageHistory()
    return chats_by_session_id[session_id]

# 6. Wrap the chain with Message History management
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 7. Start an interactive Chat Loop
print("\n--- Chef Chatbot Ready! (Type 'exit' to quit) ---\n")
session_config = {"configurable": {"session_id": "cooking_session_1"}}

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye, Chef!")
        break
        
    print("Chef: ", end="", flush=True)
    
    # We use .stream() inside our memory chain!
    for chunk in conversational_chain.stream({"input": user_input}, config=session_config):
        print(chunk.content, end="", flush=True)
    print("\n")