import requests
from constants import MAX_LENGTH

def get_random_word(level, language):

    length = length = 4 + level // 2
    if length > MAX_LENGTH:
        length = MAX_LENGTH

    url = f"https://random-word-api.herokuapp.com/word?length={length}&lang={language}"
    resp = requests.get(url)
    if resp.ok:
        data = resp.json()
        return data[0].lower()
    else:
        raise Exception("Failed to fetch word from API")
    
def format_word(word, hidden_word=None, letter=None):
    if hidden_word is None and letter is None:
        return " ".join(["_" for _ in word])
    elif hidden_word is not None and letter is not None:
        return " ".join([c if c == letter or c in hidden_word else "_" for c in word])