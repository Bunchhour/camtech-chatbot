from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Import pydatic models
from src.api.models import ChatRequest, ChatResponse
from src.bot.chain import setup_conversational_chain

# Initiailize the server
app = FastAPI(title="CamTech Chatbot API")

# Setup CORS to allow a frontend website to comunicate with this api
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # in production will put the exact domain
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# ----- Chatbot Setup -----
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# we set up the cahin once when the server starts
rag_chain = setup_conversational_chain()
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# --- API Endpoint ----
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    This is the endpoint that receives the user's message.
    It takes a ChatRequest (session_id, message) and returns a ChatResponse (answer).
    """
    try:
        # Pass the message to our Langchain bot
        response = conversational_rag_chain.invoke(
            {"input": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )

        # Package the answer into our pydantic model and return it
        return ChatResponse(answer=response["answer"])
    
    except Exception as e:
        # if sth breaks (like databae goes down), return a clean 500 Error
        raise HTTPException(status_code=500, detail=str(e))


