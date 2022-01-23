import streamlit as st 
import pickle
import requests

similarity = pickle.load(open('similarity.pkl','rb'))
movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values

def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bfaf8ff139a7c9a8096fa88b5e7e5200'.format(movie_id))

  data = response.json()
  
  return "http://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]

  distances = similarity[movie_index]

  movies_list = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6]

  recommended_movies = []
  recommended_movies_posters = []

  for i in movies_list:
    movie_id = movies.iloc[i[0]].movie_id
    
    recommended_movies.append(movies.iloc[i[0]].title)

    # now we fetch poster from API
    recommended_movies_posters.append(fetch_poster(movie_id))

  return recommended_movies, recommended_movies_posters



st.title('Discover what you want to Watch Next')

selected_movie_name = st.selectbox('TELL ME, what did you just watch',(movies_list))

if st.button('Recommend'):
  names,posters = recommend(selected_movie_name)

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

