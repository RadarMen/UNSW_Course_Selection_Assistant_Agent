"""
之前开发的parser是单纯的基于规则的分类器，负责将用户输入的问题进行分类，并根据分类结果来路由到不同的handbook类型，以便后续的向量检索和问答生成能够更有针对性地进行。
但是这个parser的能力较弱，在多种情况下用户的输入并非标准输入
因此可能输入中的关键词可能并不会被规则分类器给捕获，导致分类的结果不准确
并导致从向量数据库中获取的上下文信息不相关，最终生成的回答也不准确

因此我们需要一个更加强大的分类器
在这里，我们引入一个单独的LLM作为问题分类器，
该LLM的作用是对用户的输入进行理解分析，并返回标准JSON格式输出
此时，该标准JSON格式输出可以被后续的向量检索和问答生成模块直接使用，无需再进行额外的解析和处理
这样可以大大提升分类的准确性和系统的整体性能，同时也使得系统的架构更加清晰和模块化，便于后续的维护和扩展。
"""
import json
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
import config_data as config

class LLMQueryParserService:
    def __init__(self):
        self.chat_model = ChatTongyi(
            model = config.chat_model_name
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
你是一个 UNSW 选课辅助 Agent 的 Query Parser。
你的任务不是回答用户问题，而是把用户问题解析成标准 JSON。

你只能输出 JSON，不要输出解释，不要输出 Markdown。

JSON 格式如下：
{{
  "question_type": "prerequisite | prerequisite_check | program_requirement | course_information | study_planning | general",
  "handbook_type": "course | program | null",
  "target_course": "课程代码或 null",
  "completed_courses": ["已完成课程代码"],
  "need_vector_search": true,
  "need_metadata": true,
  "raw_query": "用户原始问题"
}}

规则：
1. 如果用户问某门课的先修课，question_type = "prerequisite"
2. 如果用户问自己是否满足某门课先修要求，question_type = "prerequisite_check"
3. 如果用户问专业、学位、学分、毕业要求，question_type = "program_requirement"
4. 如果用户问课程介绍、课程内容，question_type = "course_information"
5. 如果用户问怎么安排选课计划，question_type = "study_planning"
6. 如果无法判断，question_type = "general"

课程代码格式通常是 4 个大写字母 + 4 位数字，例如 COMP9417。
"""),
            ("user", "{query}")
        ])
    
    def safe_json_parse(self, content: str):
        """
        虽然使用一个额外的LLM作为分类器的可以提高分类的准确性
        但对于 LLM生成JSON 其最大的挑战不是LLM理解问题，而是输出格式不稳定
        因此添加一个函数，为LLM Parser增加JSON清洗功能，来提高系统的健壮性和容错性
        """
        content = content.strip()

        # 去掉'''json和'''等包裹JSON的文本
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()
        
        # 如果模型输出了额外解释，只截取第一个{到最后一个}之间的内容
        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1 and start < end:
            content = content[start:end+1]

        return json.loads(content)

    def parse(self, query: str):
        prompt = self.prompt.invoke({
            "query": query
        })

        result = self.chat_model.invoke(prompt)
        content = result.content.strip() # strip() 去掉首尾空白字符

        try:
            return self.safe_json_parse(content)
        except json.JSONDecodeError:
            # 如果解析失败，返回一个默认的结构，question_type为general，handbook_type为null，其他字段也为默认值
            return {
                "question_type": "general",
                "handbook_type": None,
                "target_course": None,
                "completed_courses": [],
                "need_vector_search": True,
                "need_metadata": False,
                "raw_query": query,
                "parser_error": content # 可以把解析失败的内容也返回，方便调试
            }
        
if __name__ == "__main__":
    parser = LLMQueryParserService()

    test_queries = [
        "COMP9417 有什么先修课？",
        "我已经修了 COMP9101，能不能选 COMP9417？",
        "AI master 一共需要多少学分？",
        "我想走计算机视觉方向，T3应该怎么选课？"
    ]

    for query in test_queries:
        print("=" * 50)
        print("用户输入:", query)
        result = parser.parse(query)
        print(result)