from flask import Flask, request, jsonify
from src.movie_service import *
from src.movie_recommendation_service import *
from src.movie_review_classification_service import *

app = Flask(__name__)

model_file_path = "models\\movie_review_classifier.pkl"
vectorizer_file_path = "models\\tf_idf_vectorizer.pkl"


@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    data = request.json
    movie_name = data["movie_name"]
    username = data["username"]
    password = data["password"]
    fetched_movie_data = read_data_from_db(username=username, password=password)
    return jsonify(recommend_movies(fetched_movie_data, movie_name=movie_name))


@app.route("/store-data", methods=["POST"])
def preprocess_and_store_data_in_db():
    data = request.json
    file_path = data["movie_file_path"]
    db_name = data["db_name"]
    username = data["username"]
    password = data["password"]
    movie_data = load_and_preprocess_data(file_path=file_path)
    conn, engine = create_db_connection(
        db_name=db_name, username=username, password=password
    )
    store_data_in_db(data=movie_data, conn=conn, engine=engine)
    return jsonify({"Status": "Success!"})


@app.route("/get-review-predictions", methods=["GET"])
def get_predictions_test():
    data = request.args
    api_key = data.get("api_key")
    movie_name = data.get("movie_name")
    movie_id = get_movie_id(movie_title=movie_name, api_key=api_key)
    imdb_id = get_imdb_id(movie_id=movie_id, api_key=api_key)
    movie_reviews = get_movie_reviews(imdb_id=imdb_id)
    result = predict_reviews(
        reviews_list=movie_reviews,
        model_file_path=model_file_path,
        vectorizer_file_path=vectorizer_file_path,
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run()
