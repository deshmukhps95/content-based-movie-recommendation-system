from flask import Flask, request, jsonify
from movie_store_service import load_and_preprocess_data, create_db_connection, store_data_in_db
from movie_recommendation_service import read_data_from_db, recommend_movies
app = Flask(__name__)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendation():
    data = request.json
    movie_name = data['movie_name']
    username = data['username']
    password = data['password']
    fetched_movie_data = read_data_from_db(username=username, password=password)
    print(fetched_movie_data.columns)
    return jsonify(recommend_movies(fetched_movie_data, movie_name=movie_name))
   
@app.route('/store_data', methods=['POST'])
def preprocess_and_store_data_in_db():
    data = request.json
    file_path = data['movie_file_path']
    db_name = data['db_name']
    username = data['username']
    password = data['password']
    movie_data = load_and_preprocess_data(file_path=file_path)
    conn, engine = create_db_connection(db_name=db_name, username=username, password=password)
    store_data_in_db(data=movie_data, conn=conn, engine=engine)
    return jsonify({"Status": "200 OK"})
    
if __name__ == '__main__': 
    app.run()