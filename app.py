import streamlit as st
from openai import OpenAI

st.title("🤖 나의 AI 챗봇")

# =========================
# 사이드바 설정
# =========================
st.sidebar.header("설정")

# OpenAI API Key 입력
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# 기분 선택 UI
mood = st.sidebar.selectbox(
    "지금 기분은 어떤가요?",
    ["😊 매우 좋음", "🙂 좋음", "😐 보통", "🙁 안 좋음", "😞 매우 안 좋음"]
)
st.session_state["mood"] = mood

# =========================
# 대화 기록 초기화
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 이전 대화 표시
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 사용자 입력 처리
# =========================
if prompt := st.chat_input("메시지를 입력하세요"):
    if not api_key:
        st.error("⚠️ 사이드바에서 API Key를 입력해주세요!")
    else:
        # 기분 정보를 system 메시지로 최초 1회 반영
        if not any(m["role"] == "system" for m in st.session_state.messages):
            st.session_state.messages.insert(
                0,
                {
                    "role": "system",
                    "content": (
                        f"사용자의 현재 기분은 '{st.session_state['mood']}' 상태이다. "
                        "이에 맞춰 공감과 응답의 톤을 조절하라."
                    )
                }
            )

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
