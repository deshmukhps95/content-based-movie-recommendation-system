import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movie_store_service import create_db_connection

def read_data_from_db(username, password):
    _, engine = create_db_connection(db_name = "movieDB", username=username, password=password)
    db_connection = engine.connect()
    return pd.read_sql("select * from movies", db_connection)

def combine_features(row):
    return row['title']+' '+row['genres']+' '+row['director']+' '+row['keywords']+' '+row['cast']

def get_cosine_similarty_matrix(df):
    features = ['genres', 'keywords', 'title', 'cast', 'director']
    for feature in features:
        df[feature] = df[feature].fillna('')
    df['combined_features'] = df.apply(combine_features, axis = 1)
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['combined_features'])
    return cosine_similarity(count_matrix)

def get_title_from_index(df, index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(df, title):
    return df[df.title == title]["movie_id"].values[0]

def recommend_movies(df, movie_name):
    recommended_movies = list()
    movie_index = get_index_from_title(df, movie_name)
    cosine_sim = get_cosine_similarty_matrix(df)
    similar_movies = list(enumerate(cosine_sim[movie_index])) 
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    i=0
    print("Top 10 similar movies to "+ movie_name+" are:\n")
    for element in sorted_similar_movies:
        print(get_title_from_index(df, element[0]))
        recommended_movies.append(get_title_from_index(df, element[0]))
        i=i+1
        if i> 9:
            break
    return {"recommended_movies": recommended_movies}
