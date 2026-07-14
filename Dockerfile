# 1. 使用带有 Python 3.11 的轻量级 Linux 镜像
FROM python:3.11-slim

# 2. 设置 Python 在容器中的运行环境
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3. 设置容器内部的工作目录
WORKDIR /app

# 4. 先单独复制依赖文件
COPY requirements.txt .

# 5. 安装 Python 依赖
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# 6. 复制后端项目代码
COPY . .

# 7. 创建运行时需要的数据目录
RUN mkdir -p /app/chroma_db /app/chat_history /app/data

# 8. 声明 FastAPI 使用的端口
EXPOSE 8000

# 9. 容器启动时执行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]