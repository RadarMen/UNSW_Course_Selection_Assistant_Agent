
---

# 基于RAG与Agent的UNSW智能选课助手

> 基于 RAG（检索增强生成）、FastAPI、向量数据库和 LLM Query Parser 构建的 UNSW 智能选课辅助 Agent。

---

# 项目简介

本项目旨在为 UNSW（University of New South Wales）学生提供一个智能选课助手。

系统能够读取 UNSW Handbook（课程手册），自动构建知识库，并结合大语言模型为学生提供课程信息查询、毕业要求查询以及选课建议。

项目目标并非构建一个简单的聊天机器人，而是逐步演化为一个能够理解用户意图并辅助进行选课规划的 AI Agent。

---

# 核心功能

## 1. Handbook上传与知识库构建

支持上传：

* Program Handbook（专业培养方案）
* Course Handbook（课程手册）

系统自动完成：

```text
PDF上传
↓
文本提取
↓
文本切分
↓
Embedding向量化
↓
Chroma向量数据库存储
```

---

## 2. Metadata信息提取

系统会自动提取课程相关元数据：

```json
{
    "university": "UNSW",
    "degree_level": "postgraduate",
    "year": "2026",
    "handbook_type": "course",
    "program": "Artificial Intelligence",
    "course_code": "COMP9417",
    "prerequisites": "COMP9101,COMP9801"
}
```

支持：

* Program分类
* Course分类
* 课程代码识别
* 先修课提取

---

## 3. RAG问答系统

系统基于 Retrieval-Augmented Generation（RAG）构建。

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
Qwen大模型推理
↓
生成回答
```

支持：

* 课程信息查询
* 专业培养方案查询
* 毕业要求查询
* Handbook内容问答

---

## 4. Query Parser（查询解析层）

为了避免所有问题都直接进入 RAG，系统新增了 Query Parser 层。

用户问题会首先被解析为结构化指令。

例如：

用户输入：

```text
我已经修了COMP9101，可以选COMP9417吗？
```

系统解析结果：

```json
{
    "question_type": "prerequisite_check",
    "target_course": "COMP9417",
    "completed_courses": [
        "COMP9101"
    ]
}
```

从而实现：

```text
自然语言
↓
结构化JSON
↓
Agent决策
```

---

## 5. Agent路由机制

系统会根据问题类型自动决定检索策略。

例如：

### 课程信息类问题

```text
COMP9517学什么？
```

自动检索：

```text
Course Handbook
```

---

### 专业要求类问题

```text
AI Master需要多少学分毕业？
```

自动检索：

```text
Program Handbook
```

---

### 先修课问题

```text
COMP9417有什么先修课？
```

自动检索：

```text
Course Handbook
+ Metadata
```

---

## 6. LLM Query Parser

除了传统规则分类器外，系统还实现了基于大语言模型的 Query Parser。

工作流程：

```text
用户问题
↓
LLM解析
↓
结构化JSON
↓
Agent决策
```

同时保留：

```text
Rule Parser
```

作为兜底方案（Fallback）。

保证系统稳定运行。

---

## 7. 会话管理

支持：

```text
Session
Conversation History
Multi-turn Chat
```

每个 Session 拥有独立对话历史。

---

## 8. 流式输出

支持：

```http
POST /chat
POST /chat/stream
```

实现类似 ChatGPT 的实时生成效果。

---

# 系统架构

```text
用户
 │
 ▼
FastAPI
 │
 ▼
Chat API
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
 ├── Session History
 └── Prompt Builder
 │
 ▼
Qwen-Max
 │
 ▼
Answer
```

---

# API接口

## 上传Handbook

```http
POST /upload
```

上传课程手册并构建知识库。

---

## 创建会话

```http
POST /session/create
```

创建新的聊天会话。

---

## 普通问答

```http
POST /chat
```

返回完整回答。

---

## 流式问答

```http
POST /chat/stream
```

实时返回生成结果。

---

## 查询聊天历史

```http
GET /chat/history/{session_id}
```

获取指定会话历史记录。

---

# 技术栈

## 后端框架

* FastAPI

## 大语言模型

* Qwen-Max
* Tongyi Chat Model

## Embedding模型

* DashScope Embedding

## 向量数据库

* ChromaDB

## Agent框架

* LangChain

## 数据存储

* Local File Storage
* Chroma Vector Store

---

# 当前完成情况

## 已完成

### RAG部分

* PDF上传
* PDF解析
* Metadata提取
* Chroma向量数据库
* 检索增强生成（RAG）

### Agent部分

* Query Parser
* Rule-based Routing
* LLM Query Parser
* Structured Query Parsing
* Agent Routing

### 工程部分

* FastAPI接口化
* Session管理
* 对话历史管理
* Streaming输出

---

## 后续规划

### 产品化

* 用户注册
* 用户登录
* 用户隔离

### Agent增强

* 学分计算
* 先修课依赖分析
* 课程关系图谱
* 自动选课规划

### 部署

* Docker部署
* 云服务器部署
* Web前端

---

# 项目目标

构建一个真正能够辅助 UNSW 学生完成：

```text
课程查询
↓
培养方案理解
↓
选课规划
↓
毕业要求分析
```

的智能选课 Agent。

---

