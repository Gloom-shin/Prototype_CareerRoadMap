import streamlit as st
import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
# 1단계: 목표 설정
st.title("커리어 로드맵 추천 챗봇")


# 세션 상태를 사용하여 단계별 진행을 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'job_responsibilities' not in st.session_state:
    st.session_state.job_responsibilities = ""
if 'job_requirements' not in st.session_state:
    st.session_state.job_requirements = ""
if 'core_skills' not in st.session_state:
    st.session_state.core_skills = []
if 'selected_skills' not in st.session_state:
    st.session_state.selected_skills = []
if 'career_activities' not in st.session_state:
    st.session_state.career_activities = []
if 'timeline' not in st.session_state:
    st.session_state.timeline = {}
if 'button_disabled' not in st.session_state:
    st.session_state.button_clicked = False
if 'experience_activity' not in st.session_state:
    st.session_state.experience_activity = ""  # 기본값 설정
if 'experience_duration' not in st.session_state:
    st.session_state.experience_duration = 1  # 기본값 설정
if 'learning_activity' not in st.session_state:
    st.session_state.learning_activity = ""  # 기본값 설정
if 'learning_duration' not in st.session_state:
    st.session_state.learning_duration = 1  # 기본값 설정

def step_1():
    st.header("1단계: 목표 설정")
    st.session_state.company_name = st.text_input("지원 회사명 (예: 네이버)", st.session_state.company_name)
    st.session_state.job_title = st.text_input("지원 직무 (예: 개발자)", st.session_state.job_title)
    st.session_state.job_responsibilities = st.text_area("지원 직무 담당업무 (채용 공고에서 복사해오세요)", st.session_state.job_responsibilities)
    st.session_state.job_requirements = st.text_area("필요 역량 및 우대사항 (채용 공고에서 복사해오세요)", st.session_state.job_requirements)

    if st.button("분석"):
        if all([st.session_state.company_name, st.session_state.job_title, st.session_state.job_responsibilities, st.session_state.job_requirements]):
            # OpenAI API를 호출하여 2단계로 이동
            with st.spinner("분석 하는 중입니다...답변 생성이 완료 되면 다음 버튼이 생성됩니다."):
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role" : "user", "content": f"""
                            지원 회사명: {st.session_state.company_name}
                            수집한 직무 : {st.session_state.job_title}의 KPI, 담당업무 :{st.session_state.job_responsibilities}, 필요역량 : {st.session_state.job_requirements} 정보를 바탕으로 요구되는 **5가지 핵심 요구사항**을 추론하여 사용자에게 제시합니다.
                            """
                        }
                    ],
                    max_tokens=3000
                )
            st.session_state.core_skills = response.choices[0].message.content
            st.session_state.step = 2
            st.button("다음 단계로 진행")
        else:
            st.warning("모든 항목을 입력해주세요.")


def step_2():
    st.header("2단계: 핵심 요구사항 선택")
    st.write(st.session_state.core_skills)

    st.session_state.selected_skills_text = st.text_area("원하는 핵심 요구사항을 1가지 이상 입력해주세요. (예시: Python, 데이터 시각화)")
    if st.button("분석"):
        print(st.session_state.selected_skills_text)
        if len(st.session_state.selected_skills_text) > 4:
            with st.spinner("분석 하는 중입니다...답변 생성이 완료 되면 다음 버튼이 생성됩니다."):
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role" : "user", "content": f"""
                                선택한 요구사항 {st.session_state.selected_skills_text} 을 기반으로 커리어 활동을 **경험 쌓기**와 **학습** 두 가지 카테고리로 각각 5가지종류씩 나누어 사용자에게 제시합니다. 이때 각 활동의 예상 활동기간(개월)도 같이 제시합니다.
                                제시전에는 무조건 이렇게 대답합니다.
                                경험쌓기활동과 학습활동 각각 1개씩 선택해주시고 몇 개월 동안 진행할 계획인지 알려주세요.
                            """
                        }
                    ],
                    max_tokens=3000
                )
            st.session_state.core_skills = response.choices[0].message.content
            print(response)
            st.session_state.step = 3
            st.button("다음 단계로 진행")
        else:
            st.warning("핵심 요구사항을 입력해주세요.")

def step_3():
    st.header("3단계: 커리어 활동 선택")
    st.write(st.session_state.core_skills)

# 경험 쌓기 활동 입력
    st.session_state.experience_activity = st.text_input("경험 쌓기 활동을 입력해주세요 (예: 프로젝트 진행)", st.session_state.experience_activity)
    
    # 학습 활동 입력
    st.session_state.learning_activity = st.text_input("학습 활동을 입력해주세요 (예:python 심화 과정 온라인 강의)", st.session_state.learning_activity)
    
    if st.button("분석"):
        if st.session_state.experience_activity and st.session_state.learning_activity:
            with st.spinner("추천할 커리어 로드맵을 생성 중입니다...답변 생성이 완료 되면 다음 버튼이 생성됩니다."):
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role" : "user", "content": f"""
                             {st.session_state.experience_activity} 경험 쌓기 활동과 
                             {st.session_state.learning_activity} 학습 활동을 기반으로 
                             각 활동을 어떻게 진행할지 하나의 월별 계획표로 제시합니다.
                            직무 전문가로써 답변을 하고, 가독성을 중시하여 답변합니다. 
                            """
                        }
                    ],
                    max_tokens=3000
                )
            st.session_state.roadmap = response.choices[0].message.content
            st.session_state.step = 4
            st.button("다음 단계로 진행")
        else:
            st.warning("경험 쌓기와 학습 활동을 모두 입력해주세요.")

def step_4():
    st.header("4단계: 커리어 로드맵 추천")
    career_roadmap = st.session_state.roadmap
    if career_roadmap:
        st.write("추천 커리어 로드맵")
        st.write(career_roadmap)
    else:
        st.warning("이전 단계에서 데이터를 입력해주세요.")
# 단계에 따라 함수 호출
if st.session_state.step == 1:
    step_1()
elif st.session_state.step == 2:
    step_2()
elif st.session_state.step == 3:
    step_3()
elif st.session_state.step == 4:
    step_4()