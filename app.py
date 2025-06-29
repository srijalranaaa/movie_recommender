import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download similarity.pkl from Google Drive if not already present
if not os.path.exists("similarity.pkl"):
    file_id = "1kATd81XtpqREWsxvt3pCdzALhDXjVVjq"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)


st.markdown("""
    <style>
    div[data-testid="column"] {
        margin-bottom: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
    <style>
    /* 🔲 Add a faded overlay behind all content */
    .stApp::before {
        content: "";
        background-image: url("https://w0.peakpx.com/wallpaper/663/269/HD-wallpaper-movie-poster-poster-collage-movie-cg.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.1;  /* 🔆 Change this to 0.1–0.4 for more/less fade */
        z-index: -1;
    }

    /* Optional: improve text readability */
    .stApp {
        color: white;
        background-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)


#  OMDb API key (your working key)
OMDB_API_KEY = "c2b7a95e"

# 🔄 New function: fetch poster using movie title
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    return data.get('Poster', "Poster not found")

# Recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movies_posters.append(fetch_poster(title))  # 👈 using title now
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.markdown("""
<h1 style='
    text-align: center;
    font-style: italic;
    color: white;
    font-weight: bold;
    text-shadow:
        -2px -2px 0 #390000,
         2px -2px 0 #390000,
        -2px  2px 0 #390000,
         2px  2px 0 #390000,
        -3px  0   0 #390000,
         3px  0   0 #390000,
         0    3px 0 #390000,
         0   -3px 0 #390000,
         0 0 10px #390000,
         0 0 20px #390000;
'>
Smartflix Movie Recommendation
</h1>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #390000;
        color: #FFFFFF;
        font-weight: bold;
        font-style: italic;
        border-radius: 8px;
        height: 3em;
        width: 20%;
        box-shadow: 1px 1px 4px #FFFFFF;
    }
    div.stButton > button:first-child:hover {
        background-color: #CD5C5C;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)



selected_movie_name = st.selectbox(
    'Select a movie to get similar recommendations',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display 10 recommended movies with custom HTML card style
    # for row in range(2):  # 2 rows
    #     cols = st.columns(5)
    #     for i in range(5):
    #         idx = row * 5 + i
    #         with cols[i]:
    for row in range(2):  # 2 rows
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            with cols[i]:
                st.markdown(f"""
                    <div style="
                        padding: 5px;
                        text-align: center;
                        font-style: italic;
                    ">
                        <img src="{posters[idx]}" style="
                            width:100%;
                            height:200px;
                            border: 2px solid #FFFFFF;  /* 🔴 red stroke */
                            box-shadow:
                            0 0 4px #390000,
                            0 0 8px #390000,
                            0 0 12px #390000;
                            border-radius: 10px;
                        "/>
                        <h4 style="color:white; margin-top:10px;">{names[idx]}</h4>
                    </div>
                """, unsafe_allow_html=True)

