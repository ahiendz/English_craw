from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_word_info():
    global words
    if request.method == 'POST':
        word = request.form.get('word')
        url = f"https://dictionary.cambridge.org/vi/dictionary/english/{word}"
        time.sleep(2)

        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all definitions
        word_means = soup.find('div', class_='def ddef_d db')
        word_ipa = soup.find('span', class_='ipa dipa lpr-2 lpl-1')

        # Extract text from each definition
        if word_means:
            word_means_text = word_means.get_text()
        else:
            word_means_text = "Không tìm thấy từ"

        if word_ipa:
            word_ipa_text = word_ipa.get_text()
        else:
            word_ipa_text = "Không tìm thấy từ"

        # Lưu từ và nghĩa vào danh sách
        words.append((word, word_means_text, word_ipa_text))

        # Kiểm tra xem đã đủ 20 từ chưa
        if len(words) % 2 == 0:
            # Tạo trang mới với bảng 5x20
            return render_template('result.html', words=words)

        return render_template('index.html', word_means=word_means_text, word_ipa=word_ipa_text)
    
    # Khởi tạo danh sách từ
    words = []
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
