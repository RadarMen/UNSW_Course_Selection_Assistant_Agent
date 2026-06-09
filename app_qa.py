import streamlit as st
from rag import RagService
import time
import config_data as config

# 设置标题
st.title("智能客服问答系统")
st.divider()    # 分隔符

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService() # 创建RagService实例，并保存到session_state中

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assisstant", "content": "您好！我是智能客服，有什么可以帮助您的吗？"}]

for msg in st.session_state["message"]:
    st.chat_message(msg["role"]).write(msg["content"])

# 在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    # 在页面输出用户提问
    st.chat_message("user").write(prompt)

    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("正在思考..."):
        response_stream = st.session_state["rag"].chain.stream({
            "input": prompt,
        },
        config = config.session_config
        )
        full_response = st.chat_message("assistant").write_stream(response_stream)
        
    st.session_state["message"].append({"role": "assistant", "content": full_response})
        # 在页面输出模型回答
        # st.session_state["message"].append({"role": "assistant", "content": response})