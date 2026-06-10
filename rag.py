from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from file_history_store import get_history

from langchain_core.messages import HumanMessage, AIMessage

class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        ) # 向量存储服务实例
        
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为基础，"
                 "简洁和专业地回答用户提供关于UNSW学校选课的问题。参考资料：{context}。"),
                ("system", "我提供对话历史记录如下："),
                MessagesPlaceholder(variable_name="history"), # 占位符，表示对话历史记录在这里，后续会通过RunnableWithMessageHistory将对话历史记录传入
                ("user","请回答用户提问：{input}。"),
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name) # 问答模型实例

        self.chain = self.__get_chain() # 最终执行链实例
    
    def __get_chain(self):
        """
        获取最终执行链
        """
        retriever = self.vector_service.get_retriever() # 获取向量检索器

        def print_prompt(full_prompt):
            print("="*20, full_prompt.to_string(), "="*20)
            return full_prompt

        def format_document(docs: list[Document]):
            if not docs:
                return "没有相关资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            return formatted_str
        
        def dict2str(value: dict) -> str:
            """
            由于conversation_chain中传出的context是一个字典对象：
            {"input":"用户输入", "history":[]}
            而这个字符串无法传入retriever中，因此需要单独将其中的input提取并转换为字符串
            再加入链中传入retriever进行检索
            """
            return value.get("input", "")
        
        def extract_history(value: dict) -> dict:
            """
            解决了输入给retriever的字符串的问题后
            发现子链字典传出给prompt_template的内容并不对
            {'input':{input:'xxxxx', 'history':[]}, 'context': 'xxxxxx'}
            这和我们在prompt_template中定义的占位符不匹配，prompt_template中占位符是{input}和{history}
            因此需要单独将history提取出来，传入prompt_template中对应的占位符位置
            """
            new_value = {}
            new_value["input"] = value["input"]["input"] # 从子链传出的字典中提取出input字符串
            new_value["context"] = value["context"] # 从子链传出的字典中提取出context字符串
            new_value["history"] = value["input"]["history"] # 从子链传出的字典中提取出history列表
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(), # 输入原样传递，不做任何处理
                "context": RunnableLambda(dict2str) | retriever | format_document, # 通过向量检索器获取上下文信息
            } | RunnableLambda(extract_history) | self.prompt_template | RunnableLambda(print_prompt) | self.chat_model | StrOutputParser() # 将输入和上下文信息通过提示模板组织好，传入问答模型进行回答
        )

        conversation_chain = RunnableWithMessageHistory(
            chain, 
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

    def ask(self, message: str, session_id: str, handbook_type: str | None = None):
        """
        这个函数是对外提供的接口，接收用户输入的消息、会话ID和手册类型（可选），并返回模型生成的回答。
        1. 首先根据handbook_type参数，决定是否使用向量检索器来获取相关的上下文信息。
        2. 如果handbook_type参数为None，则直接将用户输入的消息传入问答模型进行回答。
        3. 如果handbook_type参数不为None，则使用向量检索器来获取与用户输入相关的上下文信息，并将这些上下文信息与用户输入一起传入提示模板中，生成一个完整的提示语，然后再将这个提示语传入问答模型进行回答。
        4. 最后将模型生成的回答返回给用户。
        """
        session_config = {
            "configurable": {
                "session_id": session_id
            }
        }

        if handbook_type is None:
            return self.chain.invoke(
                {"input": message},
                config=session_config
            )
        
        retriever = self.vector_service.vector_store.as_retriever(
            # 这里的search_kwargs参数是传递给向量检索器的搜索参数，k表示返回的最相似文档数量，filter表示过滤条件，这里根据handbook_type来过滤文档，只返回handbook_type匹配的文档    
            search_kwargs={
                "k": config.similarity_threshold,
                "filter": {"handbook_type": handbook_type}
            }
        )

        docs = retriever.invoke(message)

        if not docs:
            context = "没有相关资料"
        else:
            context = ""
            for doc in docs:
                context += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
        
        prompt = self.prompt_template.invoke({
            "input": message,
            "context": context,
            "history": get_history(session_id).messages
        })

        result = self.chat_model.invoke(prompt)

        get_history(session_id).add_user_message(message)
        get_history(session_id).add_ai_message(result.content)    

        return result.content
    
    def ask_stream(
            self,
            message: str,
            session_id: str,
            handbook_type: str | None = None
    ):
        session_config = {
            "configurable": {
                "session_id": session_id
            }
        }

        if handbook_type is None:
            for chunk in self.chain.stream(
                {"input": message},
                config=session_config
            ):
                yield chunk
            return
        
        retriever = self.vector_service.vector_store.as_retriever(
            search_kwargs={
                "k": config.similarity_threshold,
                "filter": {"handbook_type": handbook_type}
            }
        )

        docs = retriever.invoke(message)
        # docs返回的是给prompt的关于上下文的文档
        # 这些文档来自于向量库中，通过向量检索器得到对应handbook_type的相关文档

        if not docs:
            context = "没有相关资料"
        else:
            context = ""
            for doc in docs:
                context += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
        
        prompt = self.prompt_template.invoke({
            "input": message,
            "context": context,
            "history": get_history(session_id).messages
        })

        full_response = ""

        for chunk in self.chat_model.stream(prompt):
            content = chunk.content
            full_response += content
            yield content
        
        history = get_history(session_id)
        history.add_messages([
            HumanMessage(content=message),
            AIMessage(content=full_response)
        ])


if __name__ == "__main__":
    # 调用前需要配置session_id，确保每个用户的对话历史记录能够正确区分开来
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    res = RagService().chain.invoke({"input": "我的身高是180cm，尺码推荐什么？"}, config=session_config)
    print(res)
