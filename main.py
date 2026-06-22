from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader
from io import BytesIO

from knowledge_base import KnowledgeBaseService
from rag import RagService

from uuid import uuid4 # 用于生成唯一的session_id

from file_history_store import get_history
from langchain_core.messages import message_to_dict

from fastapi.responses import StreamingResponse

from knowledge_base import extract_prerequisites

from database import engine
from models import Base

from sqlalchemy.orm import Session

from database import get_db
from schemas import UserRegisterRequest, UserLoginRequest, SessionCreateRequest
from auth_service import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    authenticate_user
)

from chat_service import (
    create_chat_session,
    save_chat_message,
    get_chat_messages_by_session
)

app = FastAPI(title = "UNSW Course Assistant API")

Base.metadata.create_all(bind=engine)

kb_service = KnowledgeBaseService() # 知识库服务实例
rag_service = RagService() # RAG服务实例

class ChatRequest(BaseModel):
    message: str
    session_id: str = "user_001" # 默认的session_id，可以根据实际情况进行修改
    handbook_type: str | None = None

def read_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = file.filename

    if filename.lower().endswith(".pdf"):
        content = read_pdf(file_bytes)
    elif filename.lower().endswith(".txt"):
        content = file_bytes.decode("utf-8")
    else:
        return {"success": False, "message": "只支持PDF和TXT格式的文件"}
    
    prerequisites = extract_prerequisites(content)
    
    result = kb_service.upload_by_str(content, filename)
    return {
        "success": True,
        "filename": filename,
        "message": result,
        "prerequisites": prerequisites
    }

@app.post("/session/create")
def create_session(
    request: SessionCreateRequest,
    db: Session = Depends(get_db)
    ):
    session_id = f"user_{request.user_id}_{uuid4().hex}" # 生成唯一的session_id

    chat_session = create_chat_session(
        db=db,
        user_id=request.user_id,
        session_id=session_id,
        title="新对话"
    )

    return {
        "success": True,
        "user_id": request.user_id,
        "session_id": session_id,
        "title": chat_session.title
    }
    

@app.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
    ):
    print("handbook_type:", request.handbook_type)

    result = rag_service.ask(
        message=request.message,
        session_id=request.session_id,
        handbook_type=request.handbook_type
    )

    save_chat_message(
        db=db,
        session_id=request.session_id,
        role="user",
        content=request.message
    )

    save_chat_message(
        db=db,session_id=request.session_id,
        role="assistant",
        content=result["answer"]
    )

    return {
        "success": True,
        "session_id": request.session_id,
        "question_type": result["question_type"],
        "handbook_type": result["handbook_type"],
        "query_info": result["query_info"],
        "answer": result["answer"]
    }

@app.get("/chat/history/{session_id}")
def get_chat_history(
    session_id: str, 
    db: Session = Depends(get_db)
    ):

    messages = get_chat_messages_by_session(
        db = db,
        session_id = session_id
    )

    return {
        "success": True,
        "session_id": session_id,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }
            for message in messages
        ]
    }

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    def generate():
        for chunk in rag_service.ask_stream(
            message=request.message,
            session_id=request.session_id,
            handbook_type=request.handbook_type
        ):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

@app.get("/course/{course_code}/metadata")
def get_course_metadata(course_code: str):
    metadatas = kb_service.get_course_metadata(course_code)

    return {
        "success": True,
        "course_code": course_code,
        "count": len(metadatas),
        "metadatas": metadatas
    }

@app.get("/course/{course_code}/prerequisites")
def get_course_prerequisites(course_code: str):
    prerequisites = kb_service.get_course_prerequisites(course_code)

    return {
        "success": True,
        "course_code": course_code,
        "prerequisites": prerequisites
    }


@app.post("/auth/register")
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    if get_user_by_username(db, request.username):
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )

    if get_user_by_email(db, request.email):
        raise HTTPException(
            status_code=400,
            detail="邮箱已存在"
        )

    user = create_user(
        db=db,
        username=request.username,
        email=request.email,
        password=request.password
    )

    return {
        "success": True,
        "message": "注册成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@app.post("/auth/login")
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db,
        username=request.username,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )
    
    return {
        "success": True,
        "message": "登录成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }