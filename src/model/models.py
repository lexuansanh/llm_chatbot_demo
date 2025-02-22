from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Model for handling query requests
class QueryRequest(BaseModel):
    """
    Represents a request to query the system.

    Attributes:
        question (str): The input question from the user.
    """

    question: str


# Model for handling query responses
class QueryResponse(BaseModel):
    """
    Represents the response to a query request.

    Attributes:
        question (str): The original question asked.
        answer (str): The generated answer from the system.
        image_link (List[str]): List of image links related to the response.
    """

    question: str
    answer: str
    image_link: List[str]


# Model for creating a new wish
class WishCreate(BaseModel):
    """
    Represents the data needed to create a new wish.

    Attributes:
        username (str): The name of the user creating the wish.
        wish (str): The content of the wish.
    """

    username: str
    wish: str


# Model for representing a single wish response
class WishResponse(BaseModel):
    """
    Represents a wish response with a timestamp.

    Attributes:
        username (str): The name of the user who made the wish.
        wish (str): The content of the wish.
        datetime (datetime): The timestamp when the wish was created.
    """

    username: str
    wish: str
    datetime: datetime

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects


# Model for returning a list of wishes
class WishesListResponse(BaseModel):
    """
    Represents a response containing a list of wishes.

    Attributes:
        wishes (List[WishResponse]): A list of wish responses.
    """

    wishes: List[WishResponse]
