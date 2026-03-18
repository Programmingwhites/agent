import time

import streamlit as st
from agent.react_agent import ReactAgent

#标题
st.title("智扫机器人智能客服")
st.divider()

if "agent" not in st.session_state:
     st.session_state["agent"] = ReactAgent()
if "message" not in st.session_state:
    st.session_state["message"] = []

for msg in st.session_state["message"]:
    st.chat_message(msg["role"]).write(msg["content"])

#用户输入提示词
prompt = st.chat_input();
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    response_list = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generate,cache_list):
            for chunk in generate:
                cache_list.append(chunk)
                for c in chunk:
                    time.sleep(0.01)
                    yield c
        st.chat_message("assistant").write(capture(res_stream,response_list))
        st.session_state["message"].append({"role":"assistant","content":response_list[-1]})
        st.rerun()
