import streamlit as st
import os
from openai import OpenAI

client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")



def get_ai_message(user_question):
    if 'my_assistants' not in st.session_state:
        st.session_state.my_assistants = client.beta.assistants.retrieve(assistant_id)
    if 'my_thread' not in st.session_state:
        st.session_state.thread = client.beta.threads.create()
        print( st.session_state.thread)
    ### 메시지 추가
    message = client.beta.threads.messages.create(
        thread_id= st.session_state.thread.id,
        role="user",
        content=user_question
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread.id,
        assistant_id=  st.session_state.my_assistants.id ,
    )
    while(run.status != 'completed'):
        print(run.status) 
    answer = client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id
    )
    return answer.data[0].content[0].text.value
        



st.set_page_config(page_title="커리어 로드맵 추천AI", page_icon="💬")
st.title("🗝️ 커리어 로드맵 추천")
st.caption("대화 추천1 : 커리어 로드맵 추천받고 싶어")
st.caption("대화 추천2 : 네이버 개발자가 되고 싶어")
st.caption("대화 추천3 : 상품기획 MD 커리어 로드맵 추천받고 싶어")
st.caption("대화 추천4 : 금융 영업직으로 커리어를 쌓고싶어")


# 메시지 내용 저장 
if 'message_list' not in st.session_state:
    st.session_state.message_list = []
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])


for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input("질문을 입력하세요."):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})
    with st.spinner("답변을 생성하는 중입니다..."):
        ai_message = get_ai_message(user_question)
        print(ai_message)
        with st.chat_message("ai"):
            st.write(ai_message)
        st.session_state.message_list.append({"role": "ai", "content": ai_message})

# print(f"after message_list: {st.session_state.message_list}")


