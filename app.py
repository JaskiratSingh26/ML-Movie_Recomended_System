import pandas as pd
import streamlit as st
import pickle
import requests
from jupyter_server.utils import fetch
from dotenv import load_dotenv
from openai import api_key
import os
load_dotenv()
st.title('Movie Recommender system')

working_dataframe = pd.read_csv('processed_movies.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommendations(movie_name):
    try:
        movie_index = working_dataframe[working_dataframe['title'] == movie_name].index[0]
    except IndexError:
        print(f"Movie '{movie_name}' not found in dataset.")
        return

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]
    recommended_movies = []
    print(f"\nTop recommendations for '{movie_name}':")
    for value in movie_list:
        # print(f"- {working_dataframe.iloc[value[0]].title}")
        recommended_movies.append(working_dataframe.iloc[value[0]].title)
    return recommended_movies


recommended_movies_poster_path=[]

def fecthing_movies_details(movie_id):
    api_key=os.getenv('TMDB_KEY')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)  # Or use pprint for nicer formatting
        recommended_movies_poster_path.append('https://image.tmdb.org/t/p/original'+data['poster_path'])
    else:
        print(f"Request failed with status code {response.status_code}")


option = st.selectbox(
    "How would you like to be contacted?",
    working_dataframe['title'].values
)

recommneded_movies_id_list = []


def submit(movie_name):
      recommneded_movies_id_list.append(int(working_dataframe[working_dataframe['title'] == movie_name].movie_id.values[0]))

# Display movie posters in Streamlit



if st.button("Recommend"):
    recommendations_movies = recommendations(option)

    for i in recommendations_movies:
        submit(i)

        # st.write(i)

    # st.write("You selected:", option)
    for i in recommneded_movies_id_list:
        # st.write(i)
        fecthing_movies_details(i)

    # for movie_name, poster_url in zip(recommendations_movies, recommended_movies_poster_path):
    #      # Display movie name
    #     st.image(poster_url, caption=movie_name, use_container_width=True)
    cols = st.columns(3)  # Create 5 columns for the grid layout

    for index, (movie_name, poster_url) in enumerate(zip(recommendations_movies, recommended_movies_poster_path)):
        with cols[index % 3]:  # Distribute images across columns
            st.markdown(
                f"<img src='{poster_url}' style='width:340px; height:320px;'>",
                unsafe_allow_html=True
            )
            st.write(movie_name)  # Display movie name below the image

