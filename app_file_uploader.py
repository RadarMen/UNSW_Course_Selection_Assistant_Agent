"""
基于Streamlit完成WEB网页上传服务
 pip install streamlit

 Streamlit: 当WEB页面元素发生变化，则代码重新执行一次
 重新运行可能会导致状态丢失，所以需要使用st.session_state来保存状态
 st.session_state是一个字典，可以用来保存状态信息，
 页面元素发生变化时st.session_state中的信息不会丢失，可以用来保存一些需要在页面元素发生变化时保持不变的信息，比如文件内容、文件名等
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time
from pypdf import PdfReader
from io import BytesIO

st.title("UNSW 选课资料上传服务")

uploader_file = st.file_uploader(
    label="请上传 UNSW handbook 文件",
    type=["txt", "pdf"],
    accept_multiple_files=False,
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

def read_pdf(file) -> str:
    reader = PdfReader(BytesIO(file.getvalue()))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

if uploader_file is not None:
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024
    file_type = uploader_file.type

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    if file_name.lower().endswith(".pdf"):
        file_content = read_pdf(uploader_file)
    else:
        file_content = uploader_file.getvalue().decode("utf-8")

    with st.spinner("正在上传文件到知识库..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(
            file_content,
            file_name
        )
        st.write(result)