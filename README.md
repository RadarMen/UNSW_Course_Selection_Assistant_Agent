# UNSW 选课辅助 Agent（RAG）

一个基于 RAG（Retrieval-Augmented Generation，检索增强生成）的 UNSW 选课辅助系统。

本项目基于 FastAPI、LangChain、ChromaDB 和 Qwen 构建，支持上传 UNSW handbook（课程手册）文件，并通过向量数据库实现课程信息检索与智能问答。

---

# 项目功能

## 当前 MVP 已实现功能

* 上传 UNSW handbook 文件（PDF / TXT）
* 自动文本切分与向量化
* ChromaDB 向量数据库存储
* 基于 RAG 的课程问答
* 对话历史记录支持
* 基于 session_id 的会话隔离
* 文件 MD5 去重检测
* FastAPI REST API 接口
* Swagger API 文档

---

# 技术栈

## 后端

* Python
* FastAPI
* LangChain

## 向量数据库

* ChromaDB

## 大模型与向量模型

* Qwen（通义千问）
* DashScope Embedding API

## 文档处理

* PyPDF
* RecursiveCharacterTextSplitter

---

# 项目结构

```bash
project/
│
├── main.py                     # FastAPI 入口文件
├── rag.py                      # RAG 问答链
├── knowledge_base.py           # 知识库服务
├── vector_stores.py            # 向量数据库服务
├── file_history_store.py       # 对话历史存储
├── config_data.py              # 项目配置
│
├── chroma_db/                  # Chroma 数据持久化目录
├── chat_history/               # 对话历史记录
├── md5.txt                     # 已上传文件 MD5 记录
│
├── app_qa.py                   # 旧版 Streamlit 问答页面
├── app_file_uploader.py        # 旧版 Streamlit 上传页面
```

---

# API 接口

## 1. 健康检查接口

```http
GET /health
```

返回：

```json
{
  "status": "ok"
}
```

---

## 2. 上传 Handbook

```http
POST /upload
```

支持格式：

* PDF
* TXT

文件命名示例：

```text
program_artificial_intelligence_2026.pdf
course_COMP9417_2026.pdf
```

---

## 3. 智能问答接口

```http
POST /chat
```

请求示例：

```json
{
  "message": "COMP9417 有什么先修课要求？",
  "session_id": "user_001"
}
```

返回示例：

```json
{
  "success": true,
  "session_id": "user_001",
  "answer": "..."
}
```

---

# Handbook 命名规则

系统会根据文件名自动推断 metadata。

---

## Program Handbook

命名格式：

```text
program_<program_name>_<year>.pdf
```

示例：

```text
program_artificial_intelligence_2026.pdf
```

---

## Course Handbook

命名格式：

```text
course_<course_code>_<year>.pdf
```

示例：

```text
course_COMP9417_2026.pdf
```

---

# Metadata（元数据）

当前 metadata 字段：

```python
{
    "source": filename,
    "create_time": "...",
    "university": "UNSW",
    "degree_level": "postgraduate",
    "year": "2026",
    "handbook_type": "...",
    "program": "...",
    "course_code": "..."
}
```

---

# 如何运行项目

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 2. 配置 API Key

运行前需要配置 DashScope API Key。

Windows：

```bash
set DASHSCOPE_API_KEY=your_api_key
```

Linux / Mac：

```bash
export DASHSCOPE_API_KEY=your_api_key
```

---

## 3. 启动 FastAPI 服务

```bash
uvicorn main:app --reload
```

---

## 4. 打开 Swagger 文档

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

---

# 后续计划

* 用户登录与注册系统
* 多用户隔离
* 数据库存储
* 前端页面
* 流式输出接口
* 更完善的 metadata 过滤
* 学位培养方案规划 Agent
* 多学校支持
* 课程推荐系统

---

# 项目目标

本项目旨在构建一个基于 RAG 与向量数据库的高校选课辅助系统。

长期目标是通过读取 handbook 文档，实现对不同学校的通用化支持。

---

# 声明

本项目仅用于学习与实验目的。

实际选课请以 UNSW 官方 handbook 信息为准。
