from pydantic import BaseModel, Field


class AskAgainSchema(BaseModel):
    messages: list = Field(
        default_factory=list, description="List of messages in the conversation state"
    )
    question: str = Field(
        description="Question using to ask again user to confirm or addition information to choose tools using language of user message"
    )
