import streamlit as st
from tmdbv3api import TMDb, Movie
import requests

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="나와 어울리는 영화는?", page_icon="🎬")

st.title("🎬 나와 어울리는 영화는?")
st.write("심리테스트에 기반하여 다양한 영화 추천을 제공합니다!")

st.divider()

# =========================
# 사이드바 - TMDB API Key
# =========================
st.sidebar.header("🔑 설정")
tmdb_api_key = st.sidebar.text_input("TMDB API Key", type="password")

# =========================
# 질문
# =========================
q1 = st.radio("1️⃣ 주말 계획은?", ["집에서 여유", "사람과 만나기", "즉흥 여행", "새로운 취미"])
q2 = st.radio("2️⃣ 영화 중요 요소?", ["스토리", "감정", "영상미", "유머"])
q3 = st.radio("3️⃣ 성격 타입?", ["차분", "감성형", "모험형", "낙천형"])
q4 = st.radio("4️⃣ 스트레스 해소?", ["혼자", "토론", "운동", "유머"])
q5 = st.radio("5️⃣ 결말 선호?", ["현실적", "감동", "반전", "가볍"])

st.divider()

genre_map = {
    "Action": 28, "Comedy": 35, "Drama": 18,
    "Sci-Fi": 878, "Romance": 10749, "Fantasy": 14
}

genre_scores = {k:0 for k in genre_map}

for a in [q1,q2,q3,q4,q5]:
    if a in ["집에서 여유", "스토리", "차분", "현실적"]:
        genre_scores["Drama"] += 1
    if a in ["감정", "감성형", "감동"]:
        genre_scores["Romance"] += 1
    if a in ["즉흥 여행", "모험형", "반전"]:
        genre_scores["Action"] += 1
        genre_scores["Sci-Fi"] += 1
    if a in ["유머", "낙천형"]:
        genre_scores["Comedy"] += 1
    if a in ["영상미", "새로운 취미"]:
        genre_scores["Fantasy"] += 1

# =========================
# 결과 및 API 호출
# =========================
if st.button("🎥 결과 보기"):
    if not tmdb_api_key:
        st.error("TMDB API Key를 입력하세요.")
    else:
        st.subheader("🔍 분석 중...")
        
        selected_genre = max(genre_scores, key=genre_scores.get)

        tmdb = TMDb()
        tmdb.api_key = tmdb_api_key
        tmdb.language = "ko-KR"
        movie = Movie()

        st.write(f"당신에게 어울리는 장르: **{selected_genre}**")

        # 인기 영화 (Discover)
        discover_results = movie.discover({"with_genres": genre_map[selected_genre], "sort_by": "popularity.desc"})
        top_rated_results = movie.top_rated()
        trending_results = requests.get(
            f"https://api.themoviedb.org/3/trending/movie/week?api_key={tmdb_api_key}&language=ko-KR"
        ).json().get("results", [])

        combined = discover_results + top_rated_results + trending_results
        unique_movies = {m.id:m for m in combined}  
        movie_list = list(unique_movies.values())[:10]

        for m in movie_list:
            col1, col2 = st.columns([1,3])
            with col1:
                if m.poster_path:
                    st.image("https://image.tmdb.org/t/p/w500" + m.poster_path)
            with col2:
                st.markdown(f"### {m.title}")
                st.write(f"⭐ 평점: {m.vote_average}")
                st.write(m.overview)

                reason_text = f"이 영화는 '{selected_genre}' 장르 특성 및 인기/평점 데이터를 기반으로 추천됩니다."
                st.caption(f"💡 추천 이유: {reason_text}")

            st.divider()

