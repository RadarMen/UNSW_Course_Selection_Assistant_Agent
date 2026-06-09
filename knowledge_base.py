"""
知识库基础服务代码
"""
import os 
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import re

def check_md5(md5_str: str):
    """
    检查传入的md5字符串是否已经被处理过了
    """
    if not os.path.exists(config.md5_path):
        # 进入这里说明还没有任何文件被处理过，直接返回False
        open(config.md5_path, "w", encoding="utf-8").close()  # 创建一个空的md5.txt文件
        return False    # 说明这个md5字符串没有被处理过
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():  # 读取文件中的所有行
            line = line.strip()  # 去掉行末的换行符
            if line == md5_str:  # 如果文件中的某一行和传入的md5字符串相同
                return True     # 说明这个md5字符串已经被处理过了
    return False  # 说明这个md5字符串没有被处理过

def save_md5(md5_str: str):
    """
    将传入的md5字符串，记录到文件内保存
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")  # 将md5字符串写入文件，并换行


def get_string_md5(input_str: str, encoding="utf-8"):
    """
    获取字符串的md5值
    """
    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding)
    # 计算md5值
    md5_hash = hashlib.md5(str_bytes)
    # 获取md5值的十六进制表示
    md5_hex = md5_hash.hexdigest()
    return md5_hex

def infer_handbook_type(filename: str):
    # 判断输入的handbook是program还是course
    name = filename.lower()

    if name.startswith("program"):
        return "program"
    elif name.startswith("course"):
        return "course"
    
    return "unknown"

def infer_program(filename: str):
    # 从输入的handbook文件名中，推断出这个handbook是哪个program的
    name = filename.lower()

    if name.startswith("program_"):
        program_name = filename.replace(".pdf", "").replace(".txt", "")
        program_name = program_name.replace("program_", "")
        program_name = re.sub(r"_?\d{4}$", "", program_name)
        return program_name.replace("_", " ")

    return "unknown"

def infer_course_code(filename: str):
    match = re.search(r"[A-Z]{4}\d{4}", filename.upper())
    if match:
        return match.group(0)

    return "unknown"

class KnowledgeBaseService(object):
    def __init__(self):
        # 如果文件夹不存在，就创建它
        os.makedirs(config.persist_directory, exist_ok=True)  # 确保数据持久化目录存在
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 集合名称
            persist_directory=config.persist_directory,  # 数据持久化目录
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),  # 向量化模型实例
        ) # 向量存储的实例 Chroma数据库
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, 
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len, # 计算文本长度的函数，这里使用内置的len函数
        )  # 文本分割器对象

    def upload_by_str(self, data: str, filename: str):
        """
        将传入的字符串进行向量化
        并存入向量数据库中
        """
        handbook_type = infer_handbook_type(filename)
        program = infer_program(filename)
        course_code = infer_course_code(filename)
        # 1. 首先计算这个字符串的md5值
        md5_hex = get_string_md5(data)
        # 2. 检查这个md5值是否已经被处理过了
        if check_md5(md5_hex):
            return f"文件 {filename} 已经被处理过了，跳过处理"
        if len(data) > config.max_split_char_number:
            # 3. 只对长度超过最大分割字符数量的文本进行分割
            knowledge_chunks: list[str] = self.splitter.split_text(data)  # 将文本分割成多个块
        else:
            # 4. 如果文本长度没有超过最大分割字符数量，就不进行分割，直接作为一个块
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "university": "UNSW",
            "degree_level": "postgraduate",
            "year": "2026",
            "handbook_type": handbook_type,
            "program": program,
            "course_code": course_code,
        }   

        # 5. 将分割后的文本块进行向量化，并存入向量数据库中
        self.chroma.add_texts(
            # iterable -> list \ tuple 
            # 这里的文本块列表，必须是一个可迭代对象（iterable），比如list或者tuple
            texts=knowledge_chunks,  # 文本块列表
            metadatas=[metadata for _ in knowledge_chunks],  # 为每个文本块添加元数据
        )
        # 6. 将这个md5值记录到文件中，表示这个文本已经被处理过了
        save_md5(md5_hex)

        return f"文件 {filename} 处理完成，分割成 {len(knowledge_chunks)} 个文本块，存入向量数据库中"


if __name__ == "__main__":
    # 下面是一个测试示例，演示如何使用KnowledgeBaseService类来上传一个字符串到知识库中
    service = KnowledgeBaseService()
    result = service.upload_by_str("这是一个测试文本，用于测试知识库服务的上传功能。这个文本的长度超过了最大分割字符数量，所以它会被分割成多个文本块。每个文本块都会被向量化，并存入向量数据库中。", "test.txt")
    print(result)