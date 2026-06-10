from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pypdf import PdfReader
from io import BytesIO

from knowledge_base import KnowledgeBaseService
from rag import RagService

from uuid import uuid4 # 用于生成唯一的session_id

from file_history_store import get_history
from langchain_core.messages import message_to_dict

from fastapi.responses import StreamingResponse

app = FastAPI(title = "UNSW Course Assistant API")

kb_service = KnowledgeBaseService() # 知识库服务实例
rag_service = RagService() # RAG服务实例

from knowledge_base import extract_prerequisites

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
def create_session():
    # 创建一个新的会话，并返回一个唯一的session_id
    session_id = str(uuid4()) # 生成一个唯一的session_id

    return {
        "success": True,
        "session_id": session_id
    }

@app.post("/chat")
def chat(request: ChatRequest):
    print("handbook_type:", request.handbook_type)

    session_config = {
        "configurable": {
            "session_id": request.session_id
        }
    }

    answer = rag_service.ask(
        message=request.message,
        session_id=request.session_id,
        handbook_type=request.handbook_type
    )

    return {
        "success": True,
        "session_id": request.session_id,
        "answer": answer
    }

@app.get("/chat/history/{session_id}")
def get_chat_history(session_id: str):
    history = get_history(session_id)

    messages = []
    for msg in history.messages:
        messages.append(message_to_dict(msg))

    return {
        "success": True,
        "session_id": session_id,
        "messages": messages
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