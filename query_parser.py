# 把问题分类和路由逻辑从rag.py中抽离出来，放到query_parser.py中，形成一个独立的模块，专门负责处理用户输入的问题，进行分类和路由，返回问题类型和handbook类型等元数据，
# 这样可以让代码结构更清晰，职责更单一，同时也方便后续对问题分类和路由逻辑进行修改和扩展，而不需要修改rag.py中的核心逻辑。

# updated on 2025-06-12
# 为QueryParserService增加了结构化输出
import re
from llm_query_parser import LLMQueryParserService

class QueryParserService:
    def __init__(self):
        self.use_llm_parser = True # 是否使用LLM Parser来进行问题分类和路由
        self.llm_parser = LLMQueryParserService() # LLM Parser实例

    def extract_target_course(self, message: str):
        match = re.search(r"[A-Z]{4}\d{4}", message.upper())
        if match:
            return match.group(0)
        return None
    
    def parse(self, message: str, handbook_type: str | None = None):
        if self.use_llm_parser:
            llm_result = self.llm_parser.parse(message)

            if (
                "parser_error" not in llm_result
                and llm_result.get("question_type")
                and "handbook_type" in llm_result
            ):
                if handbook_type is not None and handbook_type != "":
                    llm_result["handbook_type"] = handbook_type

                llm_result["parser_source"] = "llm"
                return llm_result
            
            print("LLM Parser failed, fallback to rule-based parser")
        
        question_type, handbook_type = self.route_question(
            message = message,
            handbook_type = handbook_type
        )

        target_course = self.extract_target_course(message)

        return {
            "question_type": question_type,
            "handbook_type": handbook_type,
            "target_course": target_course,
            "completed_courses": [], # 目前还没有做完成课程的提取，先返回一个空列表，后续可以根据需要增加这个功能
            "need_vector_search": question_type in ["prerequisite", "course_information"], # 只有当问题类型是先修课或者课程信息时，才需要向量搜索
            "need_metadata": question_type == "program_requirement", # 只有当问题类型是毕业要求时，才需要元数据
            "raw_query": message,
            "parser_source": "rule"
        }

    def classify_question(self, message: str) -> str:
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in [
            "prerequisite", "prereq", "先修", "前置课程", "能不能选", "可以选"
        ]):
            return "prerequisite"
        if any(keyword in message_lower for keyword in [
            "program", "degree", "学位", "专业", "master", "学分", "uoc", "毕业要求"
        ]):
            return "program_requirement"
        if any(keyword in message_lower for keyword in [
            "course", "课程", "comp", "math", "介绍", "内容", "学什么"
        ]):
            return "course_information"
        
        return "general"
    
    def route_question(self, message: str, handbook_type: str | None = None):
        question_type = self.classify_question(message)

        if handbook_type is None or handbook_type == "":
            if question_type == "prerequisite":
                handbook_type = "course"
            elif question_type == "program_requirement":
                handbook_type = "program"
            elif question_type == "course_information":
                handbook_type = "course"

        return question_type, handbook_type