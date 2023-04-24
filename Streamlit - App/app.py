# imports
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# Load Our Dataset


def load_data(data):
    df = pd.read_csv(data)
    return df

# st.lottie


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# RECOMMENDATTİON

def get_recommendations(df, searchterm, num_rec):
    # searchterm ile verilen filmin title sütununda var olup olmadığını kontrol edin
    if searchterm not in df['title'].unique():
        return "Movie not found. Please check your spelling."

    # searchterm ile verilen filmin id'sini alın
    movie_id = df.loc[df['title'] == searchterm]['id'].values[0]

    # movie_id ile verilen filmin benzer filmlerini getirin
    sim_movies = ['sim_movie_{}'.format(i) for i in range(1, num_rec+1)]
    sim_movies = df.loc[df['id'] == movie_id, sim_movies].values[0]

    # benzer filmlerle ilgili bilgileri bir liste içinde toplayın
    rec_movies = []
    for movie_id in sim_movies:
        movie_info = df.loc[df['id'] == movie_id]
        vote_average = movie_info['vote_average'].values[0]
        color = '#FF5733' if vote_average <= 4 else '#F5DA81' if vote_average <= 7 else '#32CD32'
        rec_movie = {'Title': movie_info['title'].values[0],
                     'Language': movie_info['Language'].values[0],
                     'Vote Average': f'{vote_average:.1f}'}
        rec_movies.append(rec_movie)

    # Create a pandas dataframe to display the recommendations in a table
    rec_movies_df = pd.DataFrame(rec_movies)

    # Display the recommendations table using Streamlit
    st.write("""
    ## Recommended Movies
    """)
    i = 1
    for rec_movie in rec_movies:
        st.title(f"""{i}-{rec_movie['Title']}""")
        i = i + 1
        st.subheader(f"""Language: {rec_movie['Language']}""")
        st.text(f"""{rec_movie['Vote Average']}""")


def main():

    st.title("Movie Recommendation App")

    menu = ["Home", "Recommend", "Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)

    df = load_data(
        "/Users/anilfurkanembel/Desktop/NLP_Movie_Recommendation/Csv Files/..\Data\movies_with_recommendation.csv")

    if choice == "Home":
        st.subheader("Home")
        netflix = load_lottieurl(
            'https://assets3.lottiefiles.com/private_files/lf30_F6EtR7.json')
        st_lottie(netflix, key='netflix')

    elif choice == "Recommend":
        st.subheader('Recommended Movies')
        searchterm = st.text_input('Last Movie You Watched')
        num_rec = st.sidebar.number_input("Number", 1, 5)

        if st.button("Recommend"):
            if searchterm is not None:
                try:
                    result = get_recommendations(df, searchterm, num_rec)
                except:
                    result = "Not Found"

            st.write(result)

    else:
        st.subheader('Analysis')
        st.text('Built with Streamlit, Pandas, Tableau')


if __name__ == '__main__':
    main()
