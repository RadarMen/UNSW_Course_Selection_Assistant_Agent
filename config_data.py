# 2026-06-01 12:00:00

# 配置文件
md5_path = "./md5.txt"


collection_name = "rag"  # 集合名称
persist_directory = "./chroma_db"  # 数据持久化目录

chunk_size = 1000  # 文本块的大小
chunk_overlap = 100  # 文本块之间的重叠部分大小
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " "]  # 文本分割的分隔符列表，优先级从高到低
max_split_char_number = 1000 # 文本分割时，单个文本块中最大的字符数量

similarity_threshold = 1 # 每次检索返回匹配的文档数量

embedding_model_name = "text-embedding-v4" # 向量化模型名称
chat_model_name = "qwen3-max" # 问答模型名称

session_config = {
    "configurable": {
        "session_id": "user_001" # 会话ID，确保每个用户的对话历史记录能够正确区分开来
    }
}