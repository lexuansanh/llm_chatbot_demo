from datetime import datetime
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.model import WishCreate, Wishes, WishResponse


def get_wishes(
    db: Session,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    limit: int = 10,
) -> List[WishResponse]:
    """
    Retrieves a list of wishes from the database based on optional time filters.

    Args:
        db (Session): The database session.
        from_time (Optional[str]): Start time filter in "YYYY-MM-DD HH:MM:SS" format. Defaults to None.
        to_time (Optional[str]): End time filter in "YYYY-MM-DD HH:MM:SS" format. Defaults to None.
        limit (int): The maximum number of wishes to retrieve. Defaults to 10.

    Returns:
        List[WishResponse]: A list of wishes matching the given criteria.
    """
    query = db.query(Wishes)

    # Apply filters for time range if provided
    if from_time:
        from_time = datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        query = query.filter(Wishes.datetime >= from_time)
    if to_time:
        to_time = datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
        query = query.filter(Wishes.datetime <= to_time)

    # Retrieve wishes sorted by datetime in descending order, limited by the given count
    wishes = query.order_by(desc(Wishes.datetime)).limit(limit).all()

    # Convert database models to response models
    return [
        WishResponse(username=w.username, wish=w.wish, datetime=w.datetime)
        for w in wishes
    ]


def create_wish(db: Session, wish_data: WishCreate) -> WishResponse:
    """
    Creates a new wish and saves it to the database.

    Args:
        db (Session): The database session.
        wish_data (WishCreate): The wish data containing username and wish text.

    Returns:
        WishResponse: The created wish with username, wish text, and timestamp.
    """
    # Create a new wish object
    new_wish = Wishes(username=wish_data.username, wish=wish_data.wish)

    # Add to database session and commit the transaction
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)  # Refresh to get updated data from the database

    # Return the created wish as a response model
    return WishResponse(
        username=new_wish.username, wish=new_wish.wish, datetime=new_wish.datetime
    )
