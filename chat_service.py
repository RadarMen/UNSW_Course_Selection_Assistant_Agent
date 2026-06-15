from sqlalchemy.orm import Session

from models import ChatSession

def create_chat_session(
        db: Session,
        user_id: int,
        session_id: str,
        title: str | None = None
):
    chat_session = ChatSession(
        user_id=user_id,
        session_id=session_id,
        title=title
    )

    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)

    return chat_session