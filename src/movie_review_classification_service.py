import pickle
import numpy as np
from src.data_preprocessor import process

import re
import urllib.request
from bs4 import BeautifulSoup
import json


def reformat_movie_title(movie_title):
    return re.sub("\s", "+", movie_title)


def get_movie_id(movie_title, api_key):
    sauce = urllib.request.urlopen(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={reformat_movie_title(movie_title)}"
    )
    soup = BeautifulSoup(sauce, "html.parser")
    site_json = json.loads(soup.text)
    return str(
        [
            d.get("id")
            for d in site_json["results"]
            if d.get("original_title") == movie_title
        ][0]
    )


def get_imdb_id(movie_id, api_key):
    sauce = urllib.request.urlopen(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    )
    soup = BeautifulSoup(sauce, "html.parser")
    site_json = json.loads(soup.text)
    return site_json["imdb_id"]


def get_movie_reviews(imdb_id):
    sauce = urllib.request.urlopen(
        "https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt".format(imdb_id)
    ).read()
    soup = BeautifulSoup(sauce, "lxml")
    soup_result = soup.find_all("div", {"class": "text show-more__control"})
    reviews_list = []
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
    return reviews_list


def predict_reviews(reviews_list, model_file_path, vectorizer_file_path):
    reviews_status = []
    clf = pickle.load(open(model_file_path, "rb"))
    vectorizer = pickle.load(open(vectorizer_file_path, "rb"))
    for review in reviews_list:
        review_np_arr = np.array([process(review)])
        movie_vector = vectorizer.transform(review_np_arr)
        pred = clf.predict(movie_vector)
        reviews_status.append("Positive" if pred else "Negative")
    return dict(zip(reviews_list, reviews_status))
