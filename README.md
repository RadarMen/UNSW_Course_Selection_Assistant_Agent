# 基于 RAG 与 Agent 的 UNSW 智能选课助手

> 一个基于 FastAPI、ChromaDB、MySQL 和大语言模型构建的 UNSW 智能选课辅助 Agent。

---

# 项目简介

本项目旨在为 UNSW 学生提供一个智能选课助手。

系统能够自动读取 UNSW Handbook（课程手册），构建课程知识库，并结合 Retrieval-Augmented Generation（RAG）与 Agent 技术，为学生提供：

- 课程信息查询
- 先修课查询
- 毕业要求查询
- Program Requirement 查询
- 多轮上下文对话
- 智能选课辅助

项目最终目标是从传统的 RAG 问答系统演化为能够辅助学生进行选课规划的 AI Agent。

---

# 核心功能

## Handbook 上传与知识库构建

支持上传：

- Program Handbook
- Course Handbook

系统自动完成：

```text
PDF上传
↓
文本提取
↓
文本切分
↓
Embedding
↓
ChromaDB存储
```

---

## Metadata 提取

系统自动提取：

```json
{
  "university": "UNSW",
  "degree_level": "postgraduate",
  "year": "2026",
  "handbook_type": "course",
  "program": "Artificial Intelligence",
  "course_code": "COMP9417",
  "prerequisites": [
    "COMP9101",
    "COMP9801"
  ]
}
```

支持：

- Program识别
- Course识别
- Course Code提取
- Prerequisite提取

---

## RAG 问答系统

工作流程：

```text
用户问题
↓
向量检索
↓
获取相关Handbook内容
↓
Prompt构建
↓
Qwen-Max
↓
生成回答
```

支持：

- 课程信息查询
- 专业培养方案查询
- 毕业要求查询
- 课程先修课查询

---

# Agent 能力

## Query Parser

系统会首先解析用户问题。

例如：

用户输入：

```text
我已经修了COMP9101，可以选COMP9417吗？
```

解析结果：

```json
{
  "question_type": "prerequisite_check",
  "target_course": "COMP9417",
  "completed_courses": [
    "COMP9101"
  ]
}
```

实现：

```text
自然语言
↓
结构化JSON
↓
Agent决策
```

---

## LLM Query Parser

除了规则分类器之外，系统新增：

- LLM Query Parser

负责：

- 问题分类
- 意图识别
- 课程提取
- 结构化输出

同时保留：

- Rule Parser

作为 Fallback。

---

## Agent Routing

系统根据问题类型自动选择检索策略。

### Program Requirement

```text
AI Master需要多少学分毕业？
```

自动检索：

```text
Program Handbook
```

### Course Information

```text
COMP9517学什么？
```

自动检索：

```text
Course Handbook
```

### Prerequisite

```text
COMP9417有什么先修课？
```

自动检索：

```text
Course Metadata
+
Course Handbook
```

---

# 用户系统

系统支持：

- 用户注册
- 用户登录
- 用户会话管理
- 聊天记录持久化

---

## 用户模型

```text
User
├── user_id
├── username
├── email
└── password
```

---

## 会话模型

```text
Chat Session
├── session_id
├── user_id
└── created_at
```

一个用户可以拥有多个对话。

例如：

```text
彭哲锴
├── AI Master毕业要求
├── COMP9417课程咨询
├── COMP9517课程咨询
└── 实习规划
```

---

## 消息模型

```text
Chat Message
├── session_id
├── role
├── content
└── created_at
```

支持：

- 多轮对话
- 上下文记忆
- 聊天历史查询

---

# 系统架构

```text
User
 │
 ▼
FastAPI
 │
 ▼
Authentication
 │
 ▼
Session Management
 │
 ▼
Query Parser Layer
 ├── LLM Query Parser
 └── Rule Parser(Fallback)
 │
 ▼
Structured Query JSON
 │
 ▼
RAG Service
 ├── Metadata Filter
 ├── Vector Retrieval
 ├── Prompt Builder
 └── History Memory
 │
 ▼
Qwen-Max
 │
 ▼
Answer
```

---

# 数据库结构

```text
users
│
│ 1 : N
│
▼
chat_sessions
│
│ 1 : N
│
▼
chat_messages
```

---

# API 接口

## 用户系统

### POST /auth/register

用户注册

### POST /auth/login

用户登录

---

## 会话管理

### POST /session/create

创建新会话

### GET /user/{user_id}/sessions

查询用户所有会话

---

## 聊天系统

### POST /chat

普通问答

### POST /chat/stream

流式问答

### GET /chat/history/{session_id}

查询聊天历史

---

## 知识库管理

### POST /upload

上传 Handbook

---

# 技术栈

## Backend

- FastAPI

## Database

- MySQL

## Vector Database

- ChromaDB

## LLM

- Qwen-Max
- Tongyi

## Framework

- LangChain

---

# 当前完成情况

## Agent MVP

- [x] PDF上传
- [x] Metadata提取
- [x] ChromaDB
- [x] RAG问答
- [x] Query Parser
- [x] LLM Query Parser
- [x] Agent Routing

---

## Product MVP

- [x] 用户注册
- [x] 用户登录
- [x] MySQL持久化
- [x] 会话管理
- [x] 聊天记录管理
- [x] 流式输出

---

## 下一步规划

### Frontend

- [ ] Vue3 前端
- [ ] 登录页
- [ ] 注册页
- [ ] 会话管理页
- [ ] 聊天页面
- [ ] Handbook上传页面

### Agent Enhancement

- [ ] 自动学分计算
- [ ] 课程依赖分析
- [ ] Program Requirement 推理
- [ ] 自动选课规划

### Deployment

- [ ] Docker
- [ ] 云服务器部署
- [ ] HTTPS

---

# 项目状态

```text
RAG MVP        ✅ 完成
Agent MVP      ✅ 完成
Product MVP    ✅ 完成

Frontend MVP   🚧 开发中
```
