from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from typing import Sequence
import json, os


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path

        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列，类似list、tuple等
        all_messages = list(self.messages)
        all_messages.extend(messages) # 将新的消息添加到现有消息列表中

        # 将数据同步写入本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 将BaseMessage转为字典对象 -> json字符串 -> 写入文件
        # 官方提供的message_to_dict方法可以将BaseMessage对象转为字典对象
        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)
        # 将数据写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f)

    @property   # 通过@property装饰器将方法变为成员属性，调用时不需要加括号
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                messages = messages_from_dict(data)
                return messages
        except FileNotFoundError:
            # 如果文件不存在，说明没有消息历史，返回空列表
            return []

    def clear(self) -> None:
        # 清空消息历史
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)