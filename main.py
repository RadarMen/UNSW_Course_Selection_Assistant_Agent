from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pypdf import PdfReader
from io import BytesIO

from knowledge_base import KnowledgeBaseService
from rag import RagService

from uuid import uuid4 # 用于生成唯一的session_id

app = FastAPI(title = "UNSW Course Assistant API")

kb_service = KnowledgeBaseService() # 知识库服务实例
rag_service = RagService() # RAG服务实例

class ChatRequest(BaseModel):
    message: str
    session_id: str = "user_001" # 默认的session_id，可以根据实际情况进行修改

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
    
    result = kb_service.upload_by_str(content, filename)
    return {
        "success": True,
        "filename": filename,
        "message": result
    }

@app.post("/session/create")
def create_session():
    session_id = str(uuid4()) # 生成一个唯一的session_id

    return {
        "success": True,
        "session_id": session_id
    }

@app.post("/chat")
def chat(request: ChatRequest):
    session_config = {
        "configurable": {
            "session_id": request.session_id
        }
    }

    answer = rag_service.chain.invoke(
        {"input": request.message},
        config=session_config
    )

    return {
        "success": True,
        "session_id": request.session_id,
        "answer": answer
    }