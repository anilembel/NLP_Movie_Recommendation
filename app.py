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

# Fxn
# Vectorize + Cosine Sim Matrix


def vectorize_text(df):
    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(df['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix,
                                   tfidf_matrix)
    return cosine_sim

# RECOMMENDATTİON


def get_recommend(title, cosine_sim, df, num_rec):
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    movie_index = indices["Deadpool"]
    similarity_scores = pd.DataFrame(
        cosine_sim[movie_index], columns=["score"])


def main():

    st.title("Movie Recommendation App")

    menu = ["Home", "Recommend", "Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)
    df = load_data("/Users/anilfurkanembel/Desktop/CleanedData.csv")

    if choice == "Home":
        st.subheader("Home")
        st.dataframe(df.head(10))

    elif choice == "Recommend":
        st.subheader('Recommended Movies')
        searchterm = st.text_input('Last Movie You Watched')

        if st.button("Recommend"):
            if searchterm is not None:
                pass

    else:
        st.subheader('Analysis')
        st.text('Built with Streamlit, Pandas, Tableau')


if __name__ == '__main__':
    main()
