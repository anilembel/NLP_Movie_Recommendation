# imports
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from streamlit_lottie import st_lottie
import requests


# for make a wide

st.set_page_config(page_title="Netflix", layout="wide")

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

    st.write("<h1 style='font-family:Netflix Sans; color:#E50914; font-size: 38px;'>NLP Movie Recommendation Project</h1>",
             unsafe_allow_html=True)

    menu = ["Home", "Recommend", "Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)
    st.sidebar.write('Anil Furkan EMBEL')
    st.sidebar.image(
        '/Users/anilfurkanembel/Desktop/NLP_Movie_Recommendation/Files/LKHU.png', width=280, )

    df = load_data(
        "/Users/anilfurkanembel/Desktop/NLP_Movie_Recommendation/Files/movies_with_recommendation.csv")

    if choice == "Home":
        netflix = load_lottieurl(
            'https://assets3.lottiefiles.com/private_files/lf30_F6EtR7.json')
        st_lottie(netflix, key='netflix')
        st.subheader('About The Project')
        st.write("<h3 style='font-family:Netflix Sans;  color:white; font-size: 18px;'>It is a project I prepared for my project that was given during my Becode training. In this project, Content based Film recommendation is given by using TF-IDF on NLP. You can write the last movie you watched by selecting the Recommend button from the menu on the left. If the movie is in the database, it will give you as many recommendations as you have chosen between 1-5.</h3>",
                 unsafe_allow_html=True)
        st.image(
            '/Users/anilfurkanembel/Desktop/NLP_Movie_Recommendation/Files/LKHU.png', width=120, )

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

        # Link of the Tableau's dashboard
        tableau_dashboard = """<div class='tableauPlaceholder' id='viz1682365090908' style='position: relative'><noscript><a href='#'><img alt='Tableau de bord 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;NL&#47;NLP_16823478959060&#47;Tableaudebord1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='NLP_16823478959060&#47;Tableaudebord1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;NL&#47;NLP_16823478959060&#47;Tableaudebord1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1682365090908');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1280px';vizElement.style.height='747px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1280px';vizElement.style.height='747px';} else { vizElement.style.width='100%';vizElement.style.height='1877px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""

        # To show the dashboard on the app

        stc.html(tableau_dashboard, width=1280, height=720)

        # Dashboard explanations


if __name__ == '__main__':
    main()
