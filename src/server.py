import uuid
from typing import Optional

import requests
import uvicorn
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.config import configsetting
from src.model import (
    QueryRequest,
    QueryResponse,
    WishCreate,
    WishesListResponse,
    WishResponse,
    get_db,
)
from src.pipelines.query_pipeline import run_query_pipeline
from src.service import create_wish, get_wishes
from src.utils.logger import logger
from src.utils.utils import update_text_with_image
from src.workflows.graph import graph

# Generate a unique thread ID
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Initialize FastAPI application
app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_api_router = APIRouter(prefix="/chat/api")


@chat_api_router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Process a query request and return a response.
    """
    try:
        result = run_query_pipeline(
            question=request.question,
            vector_store_path=configsetting.config["vector_store"]["path"],
            embedding_model=configsetting.config["embedding"]["model"],
            llm_model_name=configsetting.config["llm"]["model_name"],
        )
        return QueryResponse(
            question=request.question,
            answer=result["result"],
            documents=[doc.page_content for doc in result["source_documents"]],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_api_router.get("/")
async def home():
    """
    Health check endpoint.
    """
    return {"message": "Messenger Bot Webhook is running!"}


@chat_api_router.get("/webhook")
async def verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """
    Webhook verification for Messenger.
    """
    logger.info(f"Verifying webhook with mode: {hub_mode}, token: {hub_verify_token}")
    if hub_mode == "subscribe" and hub_verify_token == configsetting.VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@chat_api_router.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle incoming messages from Messenger.
    """
    data = await request.json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if (
                    messaging_event.get("message")
                    and messaging_event["sender"]["id"] != configsetting.BOT_ID
                ):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    logger.info(f"Received message: {message_text} from {sender_id}")
                    background_tasks.add_task(process_message, sender_id, message_text)

    return {"status": "ok"}


@chat_api_router.post("/get_answer")
async def get_answer(request: Request):
    """
    Process a user query and return an AI-generated response.
    """
    data = await request.json()
    question = data.get("question", "")
    scope = data.get("scope", "default")
    try:
        answer = graph.invoke(
            {
                "messages": [question],
                "intent": None,
                "scope": scope,
                "length_cache_response": 0,
            },
            config,
        )
        logger.info(
            f"Response:\n - Question: {question}\n - Answer: {answer['messages'][-1].content}\n"
        )
        text = answer["messages"][-1].content
        text, image_link = update_text_with_image(text)
        return QueryResponse(
            question=question,
            answer=text,
            image_link=image_link,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_api_router.get("/wishes", response_model=WishesListResponse)
def read_wishes(
    from_time: Optional[str] = Query(
        None, description="Start time for filtering wishes"
    ),
    to_time: Optional[str] = Query(None, description="End time for filtering wishes"),
    limit: int = Query(10, gt=0, description="Maximum number of wishes to retrieve"),
    db: Session = Depends(get_db),
):
    """
    Retrieve wishes within a given time range.
    """
    wishes = get_wishes(db, from_time, to_time, limit)
    return {"wishes": wishes}


@chat_api_router.post("/wishes", response_model=WishResponse)
def create_new_wish(wish_data: WishCreate, db: Session = Depends(get_db)):
    """
    Create a new wish entry.
    """
    return create_wish(db, wish_data)


async def process_message(sender_id: str, message_text: str):
    """
    Process a received message and send an appropriate reply.
    """
    try:
        answer = graph.invoke(
            {
                "messages": [message_text],
                "intent": None,
                "scope": "default",
                "length_cache_response": 0,
            },
            config,
        )
        send_message(sender_id, answer["messages"][-1].content)
    except Exception as e:
        logger.error(f"Error processing message for {sender_id}: {e}")


def send_message(recipient_id: str, text: str):
    """
    Send a response message to the user via Messenger API.
    """
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    response = requests.post(configsetting.FACEBOOK_URL, headers=headers, json=data)

    if response.status_code != 200:
        logger.error(f"Error sending message: {response.status_code}, {response.text}")


# Include the API router
app.include_router(chat_api_router)

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
