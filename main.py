import requests
from bs4 import BeautifulSoup
import time

def get_word_info(word):
    url = f"https://dictionary.cambridge.org/vi/dictionary/english/{word}"


    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all definitions
    word_means = soup.find('div', class_='def ddef_d db')
    
    # Extract text from each definition
    if word_means:
        word_means_text = word_means.get_text()
    else:
        word_means_text = "Word not found"

    return {"word": word, "mean": word_means_text}

word = "beautiful"
info = get_word_info(word)
print(info)
