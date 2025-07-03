import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# --- HEADER STYLE ---
st.markdown("""
    <style>
    .main-header {
        background-color: #390000;
        color: white;
        padding: 10px 25px;
        text-align: left;
        font-size: 24px;
        font-weight: bold;
        font-style: italic;
        font-family:  "Poppins", sans-serif;
        border-bottom: 2px solid #ffffff44;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
    }
    .spacer-header { height: 55px; }
    div.stButton > button {
        background-color: #390000 !important;
        color: white !important;
        font-weight: bold !important;
        font-style: italic !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        box-shadow: 1px 1px 4px #FFFFFF !important;
        width: 100%;
        margin-top: 8px;
    }
    div.stButton > button:hover {
        background-color: #CD5C5C !important;
    }
    </style>
    <div class="main-header">Smartflix - Movie Recommender System</div>
    <div class="spacer-header"></div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "start_done" not in st.session_state:
    st.session_state.start_done = False
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# --- DOWNLOAD similarity.pkl IF NEEDED ---
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1kATd81XtpqREWsxvt3pCdzALhDXjVVjq", "similarity.pkl", quiet=False)

# --- BACKGROUND ---
bg_url = "https://i.pinimg.com/736x/ed/d1/69/edd169fa49c08f15f4b8ef72e87d6ab5.jpg" if not st.session_state.start_done else "https://w0.peakpx.com/wallpaper/663/269/HD-wallpaper-movie-poster-poster-collage-movie-cg.jpg"
st.markdown(f"""
    <style>
    .stApp::before {{
        content: "";
        background-image: url("{bg_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.1;
        z-index: -1;
    }}
    .stApp {{
        color: white;
        background-color: transparent;
    }}
    </style>
""", unsafe_allow_html=True)

# --- LOAD MOVIE DATA ---
movies = pd.DataFrame(pickle.load(open('movies_dict.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))
OMDB_API_KEY = "c2b7a95e"

def fetch_movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    return {
        "Poster": data.get('Poster', ''),
        "Title": data.get('Title', 'N/A'),
        "Genre": data.get('Genre', 'N/A'),
        "Plot": data.get('Plot', 'N/A'),
        "imdbRating": data.get('imdbRating', 'N/A'),
        "Year": data.get('Year', 'N/A'),
        "Runtime": data.get('Runtime', 'N/A')
    }

def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:11]
    return [movies.iloc[i[0]].title for i in movie_indices]

# --- START PAGE ---
if not st.session_state.start_done:
    st.markdown("""
        <h1 style='text-align: center; font-style: italic; font-family: "Trebuchet MS", sans-serif; color: white; font-weight: bold;
        text-shadow: -2px -2px 0 #390000, 2px -2px 0 #390000, -2px 2px 0 #390000, 2px 2px 0 #390000;'>Welcome to Smartflix Movie Recommendation</h1>
        <p style='text-align: center; font-size: 20px; color: white; font-style: italic;'>
            Click <b>Start</b> to explore personalized movie recommendations!
        </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    st.markdown("""
        <hr style='border: 1px solid #ffffff33; margin-top: 40px; margin-bottom: 20px;'>
        <div style="background-color: rgba(57, 0, 0, 0.5); padding: 20px; border-radius: 15px; max-width: 850px; margin: auto; box-shadow: 0 0 8px #ffffff33;">
            <h2 style='color:#FFD700; text-align: center; font-family: "Trebuchet MS", sans-serif;'>📽️ About Smartflix</h2>
            <p style='color:white; font-size: 16px; text-align: justify; font-family: "Segoe UI", sans-serif;'>
                <b>Smartflix</b> is your intelligent movie companion, crafted to help you discover films you'll love through tailored recommendations and a seamless browsing experience.
                Whether you're into action, drama, or thrillers, Smartflix helps you explore similar movies that match your taste making movie selection easier, faster, and more enjoyable.
            </p>
            <p style='color:white; font-size: 15px; text-align: center; font-style: italic;'>
                Crafted with ❤️ by <b>Srijal </b> | 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

    with col2:
        if st.button("Start", use_container_width=True):
            import time
            with st.spinner("Loading Smartflix..."):
                time.sleep(1.5)
            st.session_state.start_done = True
            st.rerun()

# --- MOVIE DETAIL PAGE ---
elif st.session_state.selected_movie:
    data = fetch_movie_info(st.session_state.selected_movie)
    st.markdown(f"<h2 style='color:white; font-style:italic;'>🎬 {data['Title']}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**📝 Plot:** {data['Plot']}")
        st.markdown(f"**🗂️ Genre:** {data['Genre']}")
        st.markdown(f"**⭐ IMDb Rating:** {data['imdbRating']}")
        st.markdown(f"**📅 Year:** {data['Year']}")
        st.markdown(f"**⏱️ Runtime:** {data['Runtime']}")
        if st.button("🔙 Back to Smartflix"):
            st.session_state.selected_movie = None
            st.rerun()
    with col2:
        st.image(data["Poster"], use_container_width=True)

# --- MAIN RECOMMENDATION PAGE ---
else:
    st.markdown("""
        <h1 style='text-align: center; font-style: italic; color: white; font-weight: bold;
        text-shadow: -2px -2px 0 #390000, 2px -2px 0 #390000, -2px 2px 0 #390000, 2px 2px 0 #390000;'>Smartflix Movie Recommendation</h1>
    """, unsafe_allow_html=True)

    selected_movie_name = st.selectbox("Select a movie to get similar recommendations", movies['title'].values)

    if st.button('Recommend'):
        if selected_movie_name not in st.session_state.search_history:
            st.session_state.search_history.append(selected_movie_name)
        st.session_state.recommended_movies = recommend(selected_movie_name)
        st.rerun()

    if st.session_state.recommended_movies:
        if not st.session_state.selected_movie:
            st.markdown("""
                <p style='text-align: center; font-style: italic; font-size: 16px; color: white; margin-bottom: 10px;'>
                            📌Click on a movie title to view its details.
                </p>
            """, unsafe_allow_html=True)

        for row in range(0, 10, 5):
            cols = st.columns(5)
            for i in range(5):
                title = st.session_state.recommended_movies[row + i]
                with cols[i]:
                    data = fetch_movie_info(title)
                    st.image(data["Poster"], use_container_width=True)
                    if st.button(title, key=title):
                        st.session_state.selected_movie = title
                        st.rerun()

    if st.session_state.search_history:
        st.markdown("### 🔁 Your Recent Searches:")
        for title in st.session_state.search_history:
            st.markdown(f"• {title}", unsafe_allow_html=True)

# --- UNIVERSAL FOOTER (Visible on both Recommendation and Movie Info Pages, not Start Page) ---
if st.session_state.recommended_movies and st.session_state.start_done:
    st.markdown("""
        <style>
        .footer-container {
            background-color: #390000;
            color: white;
            padding: 12px 30px;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100vw;
            z-index: 9999;
            box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.5);
            border-top: 1px solid #ffffff33;
        }
        </style>
        <div class="footer-container">
            🎬 That’s a wrap! Smartflix just picked your next binge | Enjoy Smartflix 🎬 | ©2025 Smartflix Movie Recommendation </b>
        </div>
    """, unsafe_allow_html=True)










