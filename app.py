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

    # taking id of the movie which has given by searchterm
    movie_id = df.loc[df['title'] == searchterm]['id'].values[0]

    # getting similar movies which has related with the given movie_id
    sim_movies = ['sim_movie_{}'.format(i) for i in range(1, num_rec+1)]
    sim_movies = df.loc[df['id'] == movie_id, sim_movies].values[0]

    # related movie information in a list
    rec_movies = []
    for movie_id in sim_movies:
        movie_info = df.loc[df['id'] == movie_id]
        vote_average = movie_info['vote_average'].values[0]
        color = '#FF5733' if vote_average <= 4 else '#F5DA81' if vote_average <= 7 else '#32CD32'
        rec_movie = {'Title': movie_info['title'].values[0],
                     'Owerview': movie_info['overview'].values[0],
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
        st.image(
            'https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png')
        st.write(f"""<h3  style='font-family:Netflix Sans; color:Black; font-size: 24 px;'>{i}-{rec_movie['Title']}</h3>""",
                 unsafe_allow_html=True)
        st.write(f"""<h3 style='font-family:Netflix Sans; color:black; font-size: 18 px;'> Language: {rec_movie['Language']}</h3>""",
                 unsafe_allow_html=True)
        st.write(f"""<h3 style='font-family:Netflix Sans; color:red; font-size: 18 px;'> Vote: {rec_movie['Vote Average']}</h3>""",
                 unsafe_allow_html=True)
        i = i + 1

# main


def main():
    # main configs
    st.write("<h1 style='font-family:Netflix Sans; color:#E50914; font-size: 38px;'>NLP Movie Recommendation Project</h1>",
             unsafe_allow_html=True)

    menu = ["Home", "Recommend", "Analysis"]
    choice = st.sidebar.selectbox("Menu", menu)

    df = load_data(
        "Files/movies_with_recommendation.csv")

    # home page
    if choice == "Home":
        st.sidebar.image(
            'Files/Anılsidebar .png', width=300, )

        netflix = load_lottieurl(
            'https://assets1.lottiefiles.com/private_files/lf30_F6EtR7.json')
        st_lottie(netflix, key='netflix', width=1350, height=500)
        st.header('About The Project')
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>Hello I'am Anil, This is the project that my education in the field of NLP, which was given to me during the Becode Training process.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>I have completed my work on the content-based recommendation system and wehave achieved successful results on a movie dataset of 45 K  data. This system is an artificial intelligence model that can be used toprovide personalized recommendations to users.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>First of all, preprocessing steps such as cleaning the text data in the data set of the movies and tokenization were carried out. Thanks to these steps, keywords were determined for the movies.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>Then, the importance degrees of the keywords were calculated by TF-IDF method. In this way, similarity scores between films could be calculated by determining the keywords of each film.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>Finally, for a movie the user watched, the system calculated similarity scores by comparing it with other movies, and the movies with the highest similarity scores were recommended assuming they had similar characteristics to the movie the user was watching.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>All of these processes have an important role in the content-based recommendation system and can be used to provide personalized recommendations to users based on their interests.</h3>",
                 unsafe_allow_html=True)
        st.subheader('Recommendations')
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>It gives you the recommendations of the films with the closest score between 1-5 with the Model I have installed.</h3>",
                 unsafe_allow_html=True)
        st.subheader('Analysis')
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>I have prepared a dashboard where you can get more information about the movie you selected by visualizing this data with the latest Tableau. On he Dashboard:</h3>",
                 unsafe_allow_html=True)
        st.write("<h6>4 Movie recommendations</h2>", unsafe_allow_html=True)
        st.write("<h6>The Language of the Movie</h2>", unsafe_allow_html=True)
        st.write("<h6>Average Review Score</h2>", unsafe_allow_html=True)
        st.write("<h6>Genre of the movie</h2>", unsafe_allow_html=True)
        st.write("<h6>Producer Company of the Film</h2>",
                 unsafe_allow_html=True)
        st.write("<h6>The Time of Release of the Movie in the Cinema</h2>",
                 unsafe_allow_html=True)
        st.write("<h6>Movie Release Date</h2>", unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>You can learn about the information visually at a glance.</h3>",
                 unsafe_allow_html=True)
        st.write("<h3 style='font-family:Netflix Sans; color:black; font-size: 18px;'>I hope that this study will be useful for you. If you have any questions, please do not hesitate to contact with me You can directly see on the left my Linkedin and Github profile or you can just click the qr code on the dashbaord it will navigate you directly my linkedin profile.</h3>",
                 unsafe_allow_html=True)

    # recommend page
    elif choice == "Recommend":
        st.subheader('Recommended Movies')

        searchterm = st.selectbox(
            "Enter the name of a movie :", df["title"].tolist())

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
