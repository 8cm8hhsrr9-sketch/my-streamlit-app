import streamlit as st
import requests

# =========================
# 넷플릭스 스타일 CSS
# =========================
st.set_page_config(page_title="나와 닮은 영화 주인공", page_icon="🎭", layout="wide")

st.markdown("""
<style>
body {
    background-color: #141414;
    color: #ffffff;
}
.stApp {
    background-color: #141414;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
.netflix-title {
    font-size: 48px;
    font-weight: 800;
    color: #e50914;
}
.subtitle {
    color: #b3b3b3;
    font-size: 18px;
}
.movie-row {
    display: flex;
    overflow-x: auto;
    padding: 20px 0;
}
.movie-card {
    min-width: 200px;
    margin-right: 16px;
    transition: transform 0.3s;
}
.movie-card:hover {
    transform: scale(1.08);
}
.movie-title {
    font-size: 16px;
    font-weight: bold;
}
.movie-info {
    font-size: 14px;
    color: #cccccc;
}
::-webkit-scrollbar {
    height: 8px;
}
::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 헤더
# =========================
st.markdown('<div class="netflix-title">🎭 나와 닮은 영화 주인공</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신과 가장 비슷한 사람이 주인공인 영화를 추천합니다</div>', unsafe_allow_html=True)

st.divider()

# =========================
# 사이드바
# =========================
st.sidebar.header("🔑 API 설정")
tmdb_api_key = st.sidebar.text_input("TMDB API Key", type="password")

# =========================
# 질문
# =========================
questions = [
    ("문제 상황이 생기면?", ["혼자 곱씹는다", "감정적으로 반응", "몸이 먼저 움직인다", "웃음으로 넘긴다"]),
    ("영화 속 나는?", ["현실적인 인물", "사랑에 흔들리는 인물", "위험 속 인물", "이방인"]),
    ("주변의 평가는?", ["생각이 많다", "정이 많다", "행동파", "독특하다"]),
    ("끌리는 분위기", ["잔잔함", "감정 몰입", "긴장감", "몽환적"]),
    ("엔딩 취향", ["현실적 변화", "관계 정리", "문제 해결", "열린 결말"]),
    ("주인공의 핵심", ["자기 이해", "사랑", "생존", "정체성"]),
    ("나는 스스로를", ["관찰자", "감정형", "행동형", "이방인"]),
    ("스트레스 해소법", ["혼자 생각", "누군가와 대화", "움직이기", "웃기"])
]

answers = []
for i, (q, opts) in enumerate(questions, 1):
    answers.append(
        st.radio(f"{i}. {q}", opts, horizontal=True)
    )

st.divider()

# =========================
# 주인공 타입 분석
# =========================
types = {
    "현실형 관찰자": 0,
    "감정 몰입형": 0,
    "행동파 해결사": 0,
    "몽상가 / 이방인": 0,
    "유쾌한 생존자": 0
}

for a in answers:
    if a in ["혼자 곱씹는다", "현실적인 인물", "생각이 많다", "잔잔함", "현실적 변화", "자기 이해", "관찰자"]:
        types["현실형 관찰자"] += 1
    if a in ["감정적으로 반응", "사랑에 흔들리는 인물", "정이 많다", "감정 몰입", "관계 정리", "사랑", "감정형"]:
        types["감정 몰입형"] += 1
    if a in ["몸이 먼저 움직인다", "위험 속 인물", "행동파", "긴장감", "문제 해결", "생존", "행동형"]:
        types["행동파 해결사"] += 1
    if a in ["이방인", "몽환적", "열린 결말", "정체성"]:
        types["몽상가 / 이방인"] += 1
    if a == "웃음으로 넘긴다" or a == "웃기":
        types["유쾌한 생존자"] += 2

selected_type = max(types, key=types.get)

type_to_genre = {
    "현실형 관찰자": 18,
    "감정 몰입형": 10749,
    "행동파 해결사": 28,
    "몽상가 / 이방인": 14,
    "유쾌한 생존자": 35
}

# =========================
# 결과
# =========================
if st.button("🎬 나와 닮은 주인공 찾기"):
    if not tmdb_api_key:
        st.error("TMDB API Key를 입력해주세요.")
    else:
        st.markdown(f"## 👤 당신은 **{selected_type}** 타입입니다")

        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={tmdb_api_key}"
            f"&with_genres={type_to_genre[selected_type]}"
            f"&sort_by=vote_average.desc"
            f"&vote_count.gte=100"
            f"&language=ko-KR"
        )

        movies = requests.get(url).json().get("results", [])[:10]

        st.markdown("## 🍿 지금 당신에게 어울리는 영화들")

        st.markdown('<div class="movie-row">', unsafe_allow_html=True)
        for m in movies:
            if not m.get("poster_path"):
                continue
            poster = "https://image.tmdb.org/t/p/w500" + m["poster_path"]

            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" width="200">
                <div class="movie-title">{m['title']}</div>
                <div class="movie-info">⭐ {m['vote_average']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

