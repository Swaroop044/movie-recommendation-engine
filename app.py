import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4b07ff33fc201c142df8f50047a135e7&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']  # Adjusted column name if it's 'id'
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Check the columns of the DataFrame
# st.write(movies.columns)  # Include this line to verify the columns
def get_netflix_url(movie_title):
    # Replace spaces with "+" to create a query for Netflix search page
    search_query = movie_title.replace(" ", "+")
    # Construct the search URL for Netflix (you may need to adjust this)
    return f"https://www.justwatch.com/in/search?q={search_query}"
    # https: // www.justwatch.com / in / search?q = aliens
    # return f"https://www.netflix.com/in/title/81476453"
# st.title('Cinematic Recommendation Engine')

st.markdown(
    "<h1 style='text-align: center; font-size: 36px;'>Cinematic Recommendation Engine</h1>",
    unsafe_allow_html=True
)
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f"[![{names[i]}]({posters[i]})]({get_netflix_url(names[i])})", unsafe_allow_html=True)
            st.text(names[i])

    # with col1:
    #     st.text(names[0])
    #     st.markdown(f"[![{names[i]}]({posters[i]})]({get_netflix_url(names[i])})", unsafe_allow_html=True)
    #     st.image(posters[0])
    #
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    #
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    #
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    #
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
