import streamlit as st
import requests

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="나와 어울리는 영화는?", page_icon="🎬")

st.title("🎬 나와 어울리는 영화는?")
st.write("당신의 영화 취향을 바탕으로, 지금 가장 잘 맞는 영화를 추천해드려요.")

st.divider()

# =========================
# 사이드바 - TMDB API Key
# =========================
st.sidebar.header("🔑 설정")
tmdb_api_key = st.sidebar.text_input("TMDB API Key", type="password")

# =========================
# 장르 점수 초기화
# =========================
genre_scores = {
    "액션": 0,
    "코미디": 0,
    "드라마": 0,
    "SF": 0,
    "로맨스": 0,
    "판타지": 0
}

# =========================
# 질문 (영화 추천 최적화)
# =========================
q1 = st.radio(
    "1️⃣ 영화를 볼 때, 가장 끌리는 분위기는?",
    [
        "손에 땀을 쥐게 하는 긴장감",
        "가볍게 웃으며 볼 수 있는 분위기",
        "현실적이고 깊은 감정선",
        "상상력을 자극하는 세계관"
    ]
)

q2 = st.radio(
    "2️⃣ 영화가 끝난 후, 어떤 여운이 남는 게 좋나요?",
    [
        "속이 뻥 뚫리는 통쾌함",
        "기분이 좋아지는 따뜻함",
        "곱씹게 되는 묵직함",
        "‘와…’ 하고 감탄하게 되는 설정"
    ]
)

q3 = st.radio(
    "3️⃣ 선호하는 영화 전개 방식은?",
    [
        "빠르고 역동적인 전개",
        "웃음 포인트가 자주 나오는 전개",
        "인물 중심의 서사",
        "현실을 벗어난 독특한 이야기"
    ]
)

q4 = st.radio(
    "4️⃣ 영화 속에서 가장 중요한 요소는?",
    [
        "액션과 스케일",
        "캐릭터의 매력",
        "감정 몰입과 연기",
        "세계관과 설정"
    ]
)

q5 = st.radio(
    "5️⃣ 지금 보고 싶은 영화는 어떤 기분에 가깝나요?",
    [
        "에너지를 끌어올리고 싶다",
        "아무 생각 없이 즐기고 싶다",
        "조용히 몰입하고 싶다",
        "새로운 세계로 떠나고 싶다"
    ]
)

# =========================
# 답변 → 장르 점수 매핑
# =========================
answer_map = {
    q1: {
        "손에 땀을 쥐게 하는 긴장감": ["액션"],
        "가볍게 웃으며 볼 수 있는 분위기": ["코미디"],
        "현실적이고 깊은 감정선": ["드라마", "로맨스"],
        "상상력을 자극하는 세계관": ["SF", "판타지"],
    },
    q2: {
        "속이 뻥 뚫리는 통쾌함": ["액션"],
        "기분이 좋아지는 따뜻함": ["코미디", "로맨스"],
        "곱씹게 되는 묵직함": ["드라마"],
        "‘와…’ 하고 감탄하게 되는 설정": ["SF", "판타지"],
    },
    q3: {
        "빠르고 역동적인 전개": ["액션"],
        "웃음 포인트가 자주 나오는 전개": ["코미디"],
        "인물 중심의 서사": ["드라마", "로맨스"],
        "현실을 벗어난 독특한 이야기": ["SF", "판타지"],
    },
    q4: {
        "액션과 스케일": ["액션"],
        "캐릭터의 매력": ["코미디", "로맨스"],
        "감정 몰입과 연기": ["드라마"],
        "세계관과 설정": ["SF", "판타지"],
    },
    q5: {
        "에너지를 끌어올리고 싶다": ["액션"],
        "아무 생각 없이 즐기고 싶다": ["코미디"],
        "조용히 몰입하고 싶다": ["드라마", "로맨스"],
        "새로운 세계로 떠나고 싶다": ["SF", "판타지"],
    }
}

for question, mapping in answer_map.items():
    for genre in mapping.get(question, []):
        genre_scores[genre] += 1

# =========================
# TMDB 장르 ID
# =========================
genre_id_map = {
    "액션": 28,
    "코미디": 35,
    "드라마": 18,
    "SF": 878,
    "로맨스": 10749,
    "판타지": 14
}

st.divider()

# =========================
# 결과 보기
# =========================
if st.button("🎥 결과 보기"):
    if not tmdb_api_key:
        st.error("사이드바에 TMDB API Key를 입력해주세요.")
    else:
        selected_genre = max(genre_scores, key=genre_scores.get)
        genre_id = genre_id_map[selected_genre]

        st.subheader("🔍 분석 결과")
        st.write(f"당신에게 가장 잘 어울리는 장르는 **{selected_genre}** 입니다.")

        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={tmdb_api_key}"
            f"&with_genres={genre_id}"
            f"&language=ko-KR"
            f"&sort_by=popularity.desc"
        )

        response = requests.get(url).json()
        movies = response.get("results", [])[:5]

        st.divider()
        st.subheader("🎬 추천 영화")

        for movie in movies:
            col1, col2 = st.columns([1, 3])

            with col1:
                if movie.get("poster_path"):
                    poster_url = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
                    st.image(poster_url, use_column_width=True)

            with col2:
                st.markdown(f"### {movie.get('title')}")
                st.write(f"⭐ 평점: {movie.get('vote_average')}")
                st.write(movie.get("overview", "줄거리 정보가 없습니다."))
                st.caption(
                    f"💡 추천 이유: 당신은 **{selected_genre}** 장르에서 "
                    "몰입감과 만족감을 느끼는 경향이 있어요."
                )

            st.divider()
