import pandas as pd
import psycopg2
from src.data_preprocessor import process
from sqlalchemy import create_engine


def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path, low_memory=False)
    for col in data.columns:
        if col != "title":
            data[col] = data.apply(lambda row: process(row[col]), axis=1)
    return data


def create_db_connection(db_name, username, password):
    conn = psycopg2.connect(
        database=db_name,
        user=username,
        password=password,
        host="localhost",
        port="5432",
    )
    conn.autocommit = True
    engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}"
    )
    return conn, engine


def store_data_in_db(data, conn, engine):
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS MOVIES(movie_id int NOT NULL,
                                            genres VARCHAR(30),
                                            keywords VARCHAR(100),
                                            title VARCHAR(30), 
                                            director VARCHAR(30));"""
    cursor.execute(sql)
    try:
        data.to_sql("movies", engine, if_exists="replace", index=False)
        print("Data stored successfully!")
    except:
        print("Unable to store data. Some error occured!")
    finally:
        engine.dispose()
    conn.commit()
    conn.close()
