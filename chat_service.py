from sqlalchemy.orm import Session
from models import ChatSession, ChatMessage

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

def save_chat_message(
        db: Session,
        session_id: str,
        role: str,
        content: str
):
    message = ChatMessage(
        session_id = session_id,
        role = role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_chat_messages_by_session(
        db: Session,
        session_id: str
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

def get_chat_sessions_by_user(
        db: Session,
        user_id: int    
):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )