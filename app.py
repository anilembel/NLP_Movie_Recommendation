# imports
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Our Dataset


def load_data(data):
    df = pd.read_csv(data)
    return df


# RECOMMENDATTİON

def get_recommendations(df, searchterm, num_rec):
    # searchterm ile verilen filmin title sütununda var olup olmadığını kontrol edin
    if searchterm not in df['title'].unique():
        return "Movie not found. Please check your spelling."

    # searchterm ile verilen filmin id'sini alın
    movie_id = df.loc[df['title'] == searchterm]['id'].values[0]

    # movie_id ile verilen filmin benzer filmlerini getirin
    sim_movies = ['sim_movie_{}'.format(i) for i in range(1, 6)]
    sim_movies = df.loc[df['id'] == movie_id, sim_movies].values[0]

    # benzer filmlerle ilgili bilgileri bir liste içinde toplayın
    rec_movies = []
    for movie in sim_movies:
        movie_info = df.loc[df['id'] == movie, 'title'].values[0]
        rec_movies.append(movie_info)

    # istenen sayıda öneri listesini döndürün
    return rec_movies[:num_rec]


def main():

    st.title("Movie Recommendation App")

    menu = ["Home", "Recommend", "Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)

    df = load_data(
        "/Users/anilfurkanembel/Desktop/NLP_Movie_Recommendation/..\Data\movies_with_recommendation.csv")

    if choice == "Home":
        st.subheader("Home")
        st.dataframe(df.head(10))

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
