import pickle
import streamlit as st
import requests

# Fetch movie poster from the API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Movie recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_ids.append(movies.iloc[i[0]].movie_id)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# Set up the Streamlit page
st.set_page_config(page_title="My Movie Partner", layout="wide")

# Add custom CSS styling for better appearance
st.markdown("""
    <style>
        body {
            background-color: #1a1a1d;
            color: #e0e0e0;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #f24e1e;
            color: white;
            border-radius: 10px;
            font-size: 18px;
        }
        .stSelectbox>div>div {
            background-color: #2c2f38;
            color: #e0e0e0;
            font-size: 18px;
        }
        h1 {
            font-family: 'Helvetica', sans-serif;
            color: #f24e1e;
        }
        .stText {
            color: #f24e1e;
            font-size: 18px;
            text-align: center;
        }
        .stImage {
            border-radius: 10px;
        }
        .stColumns>div {
            background-color: #2c2f38;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Main title of the application
st.title('My Movie Partner')

# Load data and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values

# Movie selection dropdown
selected_movie = st.selectbox(
    "Select a movie to find your next favorite:",
    movie_list
)

# Recommendation button
if st.button('Get Movie Recommendations'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)
    
    # Display the recommended movies in a stylish grid layout with links
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.markdown(f"[![{recommended_movie_names[0]}]({recommended_movie_posters[0]})](https://www.themoviedb.org/movie/{recommended_movie_ids[0]})", unsafe_allow_html=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.markdown(f"[![{recommended_movie_names[1]}]({recommended_movie_posters[1]})](https://www.themoviedb.org/movie/{recommended_movie_ids[1]})", unsafe_allow_html=True)
    with col3:
        st.text(recommended_movie_names[2])
        st.markdown(f"[![{recommended_movie_names[2]}]({recommended_movie_posters[2]})](https://www.themoviedb.org/movie/{recommended_movie_ids[2]})", unsafe_allow_html=True)
    with col4:
        st.text(recommended_movie_names[3])
        st.markdown(f"[![{recommended_movie_names[3]}]({recommended_movie_posters[3]})](https://www.themoviedb.org/movie/{recommended_movie_ids[3]})", unsafe_allow_html=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.markdown(f"[![{recommended_movie_names[4]}]({recommended_movie_posters[4]})](https://www.themoviedb.org/movie/{recommended_movie_ids[4]})", unsafe_allow_html=True)
