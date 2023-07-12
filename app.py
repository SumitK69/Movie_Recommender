import streamlit as st
import pickle
import pandas as pd
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = pd.DataFrame(movies)

movies_title = movies_list['title'].values
# similarity = pickle.load(open('', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=a5fad6ea2f6605bb54377680355f0e1c&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in recommended_list:
        # fetching poster
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.title("Movie Recommender System")

selected_movie_name = st.selectbox('Movies', movies_title)

if st.button('recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
