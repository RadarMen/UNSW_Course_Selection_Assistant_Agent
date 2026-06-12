# 把问题分类和路由逻辑从rag.py中抽离出来，放到query_parser.py中，形成一个独立的模块，专门负责处理用户输入的问题，进行分类和路由，返回问题类型和handbook类型等元数据，
# 这样可以让代码结构更清晰，职责更单一，同时也方便后续对问题分类和路由逻辑进行修改和扩展，而不需要修改rag.py中的核心逻辑。

# updated on 2025-06-12
# 为QueryParserService增加了结构化输出
import re

class QueryParserService:
    def extract_target_course(self, message: str):
        match = re.search(r"[A-Z]{4}\d{4}", message.upper())
        if match:
            return match.group(0)
        return None
    
    def parse(self, message: str, handbook_type: str | None = None):
        question_type, routed_handbook_type = self.route_question(
            message=message,
            handbook_type=handbook_type
        )

        target_course = self.extract_target_course(message)

        return {
            "question_type": question_type,
            "handbook_type": routed_handbook_type,
            "target_course": target_course
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