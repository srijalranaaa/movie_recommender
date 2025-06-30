import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    file_id = "1kATd81XtpqREWsxvt3pCdzALhDXjVVjq"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)


# SET SESSION STATE
if "start_done" not in st.session_state:
    st.session_state.start_done = False


#  SELECT BACKGROUND IMAGE BASED ON PAGE
if not st.session_state.start_done:
    bg_url = "https://i.pinimg.com/736x/ed/d1/69/edd169fa49c08f15f4b8ef72e87d6ab5.jpg"
else:
    bg_url = "https://w0.peakpx.com/wallpaper/663/269/HD-wallpaper-movie-poster-poster-collage-movie-cg.jpg"


# APPLY BACKGROUND STYLE (SAME STYLE BOTH PAGES)
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
    button {{
        background-color: #390000 !important;
        color: white !important;
        font-weight: bold !important;
        font-style: italic !important;
        border-radius: 8px !important;
        height: 3em !important;
        box-shadow: 1px 1px 4px #FFFFFF !important;
        font-size: 18px !important;
    }}
    button:hover {{
        background-color: #CD5C5C !important;
    }}
    </style>
""", unsafe_allow_html=True)


#  START PAGE
if not st.session_state.start_done:
    st.markdown("""
        <h1 style='text-align: center; font-style: italic; font-family: "Trebuchet MS", "Segoe UI", sans-serif; color: white; font-weight: bold;
        text-shadow: -2px -2px 0 #390000, 2px -2px 0 #390000, -2px 2px 0 #390000, 2px 2px 0 #390000,
        -3px 0 0 #390000, 3px 0 0 #390000, 0 3px 0 #390000, 0 -3px 0 #390000,
        0 0 10px #390000, 0 0 20px #390000;'>Welcome to Smartflix Movie Recommendations 🎬</h1>
        <p style='text-align: center; font-size: 20px; color: white; font-style: italic;'>
            Click the <b>Start</b> button to explore movie recommendations tailored just for you!
        </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start = st.button("Start", use_container_width=True)
        import time  # ✅ Make sure this is at the top

        if start:
            with st.spinner("Loading Smartflix..."):
                time.sleep(1.7)  # ⏳ Gives a smoother feel
            st.session_state.start_done = True
            st.rerun()



#  MAIN PAGE (AFTER CLICKING START)
else:
    # Load movie data
    movies_dict = pickle.load(open('movies_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl','rb'))

    OMDB_API_KEY = "c2b7a95e"

    def fetch_poster(title):
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()
        return data.get('Poster', "Poster not found")

    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            title = movies.iloc[i[0]].title
            recommended_movies.append(title)
            recommended_movies_posters.append(fetch_poster(title))
        return recommended_movies, recommended_movies_posters

    st.markdown("""
        <h1 style='text-align: center; font-style: italic; color: white; font-weight: bold;
         text-shadow: -2px -2px 0 #390000, 2px -2px 0 #390000, -2px 2px 0 #390000, 2px 2px 0 #390000,
        -3px 0 0 #390000, 3px 0 0 #390000, 0 3px 0 #390000, 0 -3px 0 #390000,
        0 0 10px #390000, 0 0 20px #390000;'>Smartflix Movie Recommendation</h1>
    """, unsafe_allow_html=True)

    selected_movie_name = st.selectbox(
        'Select a movie to get similar recommendations',
        movies['title'].values
    )

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        for row in range(2):  # 2 rows
            cols = st.columns(5)
            for i in range(5):
                idx = row * 5 + i
                with cols[i]:
                    st.markdown(f"""
                        <div style="padding: 5px; text-align: center; font-style: italic;">
                            <img src="{posters[idx]}" style="width:100%; height:200px;
                                border: 2px solid #FFFFFF;
                                box-shadow: 0 0 4px #390000, 0 0 8px #390000, 0 0 12px #390000;
                                border-radius: 10px;" />
                            <h4 style="color:white; margin-top:10px;">{names[idx]}</h4>
                        </div>
                    """, unsafe_allow_html=True)




