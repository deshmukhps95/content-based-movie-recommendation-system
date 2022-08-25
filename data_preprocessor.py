import nltk
import re
import unicodedata
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from string import digits
import warnings
warnings.filterwarnings('ignore')

def strip_html_tags(text: str):
    try:
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text()
    except Exception as e:
        return text
    return stripped_text


def remove_accented_chars(text: str):
    try:
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8", "ignore")
        )
    except Exception as e:
        return text
    return text

def remove_url(statement: str):
    patterns = [r"http\S+", r"www\S+"]
    out = statement
    for pattern in patterns:
        out = re.sub(pattern, "", out)
    return out


def tokenize_statement(statement: str):
    tokens = nltk.word_tokenize(statement)
    return " ".join(token for token in tokens)


def strip_punctuation(statement: str):
    regex = re.compile("[%s]" % re.escape(string.punctuation))
    statement = regex.sub(" ", statement)
    return statement


def lower_case_statement(statement: str):
    return statement.lower()

def remove_stop_words(statement: str):
    stop_words = set(stopwords.words("english"))
    word_tokens = statement.split()
    filtered_statement = " ".join(w for w in word_tokens if w not in stop_words)
    return filtered_statement


def remove_special_characters(text: str, remove_digits=False):
    pattern = r"[^a-zA-z0-9\s]" if not remove_digits else r"[^a-zA-z\s]"
    text = re.sub(pattern, "", text)
    return text

def process(statement):
    try:
        statement = strip_html_tags(statement)
        statement = remove_accented_chars(statement)
        statement = strip_punctuation(statement)
        statement = remove_url(statement)
        statement = tokenize_statement(statement)
        statement = lower_case_statement(statement)
    except Exception as e:
        pass
    return statement