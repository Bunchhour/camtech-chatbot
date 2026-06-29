import warnings
# suppose deprecation warnings from langchian
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.bot.chain import setup_conversational_chain

# A dctionary to store sewssion (so multiple users could chat at once)
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
    
def main():
    print("Setting up the CamTech Chatbot...")
    try:
        rag_chain = setup_conversational_chain()
    except Exception as e:
        print(f"Failed to setup chatbot. Is your datbase running and API keys set? Error: {e}")
        return
    
    # Wrap our chain with the history tracker
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    print("\n" + "="*50)
    print("🎓 Welcome to the CamTech University Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("="*50 + "\n")

    session_id = "user_123"

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue
            
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )
            print(f"\nBot: {response['answer']}\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()