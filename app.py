import streamlit as st
import requests
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="나와 닮은 영화 주인공은?", page_icon="🎭")

# =========================
# 세션 상태 초기화
# =========================
if "page" not in st.session_state:
    st.session_state.page = "test"

if "result_data" not in st.session_state:
    st.session_state.result_data = None

# =========================
# 사이드바
# =========================
st.sidebar.header("🔑 설정")
tmdb_api_key = st.sidebar.text_input("TMDB API Key", type="password")

# ======================================================
# 🧠 심리테스트 화면
# ======================================================
if st.session_state.page == "test":

    st.title("🎭 나와 닮은 영화 주인공은?")
    st.write("당신과 가장 비슷한 사람이 주인공으로 등장하는 영화를 추천해드립니다.")
    st.divider()

    # =========================
    # 질문
    # =========================
    q1 = st.radio("1️⃣ 문제 상황이 생기면 당신은?",
        ["혼자 곱씹으며 해결책을 찾는다", "감정적으로 먼저 반응한다", "몸이 먼저 움직인다", "상황을 웃음으로 넘긴다"])

    q2 = st.radio("2️⃣ 당신이 영화 속 주인공이라면?",
        ["평범한 일상 속 인물", "사랑이나 관계로 흔들리는 인물", "위험한 상황에 놓인 인물", "세상과 어딘가 어긋난 인물"])

    q3 = st.radio("3️⃣ 주변 사람들이 자주 하는 말은?",
        ["생각이 많다", "정이 많다", "행동력이 좋다", "독특하다"])

    q4 = st.radio("4️⃣ 당신의 인생 영화 주인공은?",
        ["현실적인 고민을 하는 사람", "상처받고 사랑하는 사람", "싸우고 도망치고 극복하는 사람", "자기만의 세계가 있는 사람"])

    q5 = st.radio("5️⃣ 분위기로 더 끌리는 영화는?",
        ["잔잔하고 현실적인", "감정적으로 몰입되는", "긴장감 넘치는", "몽환적이고 낯선"])

    q6 = st.radio("6️⃣ 당신은 어떤 엔딩이 더 당신답나요?",
        ["현실은 그대로지만 내가 변한다", "관계가 정리된다", "문제를 해결하고 앞으로 나아간다", "명확하지 않아도 괜찮다"])

    q7 = st.radio("7️⃣ 영화 주인공에게 중요한 것은?",
        ["자기 이해", "사랑과 관계", "생존과 선택", "정체성과 자유"])

    q8 = st.radio("8️⃣ 당신은 스스로를 어떻게 생각하나요?",
        ["현실적인 관찰자", "감정적인 사람", "행동파", "이방인 같은 존재"])

    # =========================
    # 결과 버튼
    # =========================
    if st.button("🎬 나와 닮은 주인공 찾기"):
        if not tmdb_api_key:
            st.error("TMDB API Key를 입력해주세요.")
        else:
            # ===== 기존 로직 (변경 없음) =====
            archetypes = {
                "현실형 관찰자": 0,
                "감정 몰입형": 0,
                "행동파 해결사": 0,
                "몽상가 / 이방인": 0,
                "유쾌한 생존자": 0
            }

            answers = [q1, q2, q3, q4, q5, q6, q7, q8]

            for a in answers:
                if a in ["혼자 곱씹으며 해결책을 찾는다", "평범한 일상 속 인물", "생각이 많다", "현실적인 고민을 하는 사람", "잔잔하고 현실적인", "현실은 그대로지만 내가 변한다", "자기 이해", "현실적인 관찰자"]:
                    archetypes["현실형 관찰자"] += 1
                if a in ["감정적으로 먼저 반응한다", "사랑이나 관계로 흔들리는 인물", "정이 많다", "감정적으로 몰입되는", "관계가 정리된다", "사랑과 관계", "감정적인 사람"]:
                    archetypes["감정 몰입형"] += 1
                if a in ["몸이 먼저 움직인다", "위험한 상황에 놓인 인물", "행동력이 좋다", "긴장감 넘치는", "문제를 해결하고 앞으로 나아간다", "생존과 선택", "행동파"]:
                    archetypes["행동파 해결사"] += 1
                if a in ["세상과 어딘가 어긋난 인물", "독특하다", "몽환적이고 낯선", "명확하지 않아도 괜찮다", "정체성과 자유", "이방인 같은 존재"]:
                    archetypes["몽상가 / 이방인"] += 1
                if a == "상황을 웃음으로 넘긴다":
                    archetypes["유쾌한 생존자"] += 2

            selected_type = max(archetypes, key=archetypes.get)

            type_to_genre = {
                "현실형 관찰자": 18,
                "감정 몰입형": 10749,
                "행동파 해결사": 28,
                "몽상가 / 이방인": 14,
                "유쾌한 생존자": 35
            }

            url = (
                f"https://api.themoviedb.org/3/discover/movie"
                f"?api_key={tmdb_api_key}"
                f"&with_genres={type_to_genre[selected_type]}"
                f"&language=ko-KR"
                f"&sort_by=vote_average.desc"
                f"&vote_count.gte=100"
            )

            movies = requests.get(url).json().get("results", [])[:10]

            # 결과 저장 & 페이지 전환
            st.session_state.result_data = (selected_type, movies)
            st.session_state.page = "result"
            st.rerun()

# ======================================================
# 🎥 결과 화면
# ======================================================
if st.session_state.page == "result":

    selected_type, movies = st.session_state.result_data

    with st.spinner("🎬 당신과 닮은 영화 주인공을 찾고 있습니다..."):
