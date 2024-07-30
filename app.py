from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# Khởi tạo danh sách từ ngoài hàm để không bị mất khi refresh
words = []

@app.route('/', methods=['GET', 'POST'])
def get_word_info():
    global words
    if request.method == 'POST':
        word = request.form.get('word')
        if not word:
            return render_template('index.html', error="Please enter a word.")

        url = f"https://dictionary.cambridge.org/vi/dictionary/english/{word}"
        time.sleep(1)

        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except requests.RequestException as e:
            return render_template('index.html', error="Failed to retrieve data from dictionary.")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all definitions and IPA
        word_means = soup.find('div', class_='def ddef_d db')
        word_ipa = soup.find('span', class_='ipa dipa lpr-2 lpl-1')

        # Extract text from each definition
        word_means_text = word_means.get_text() if word_means else "Không tìm thấy nghĩa"
        word_ipa_text = word_ipa.get_text() if word_ipa else "Không tìm thấy IPA"

        # Lưu từ và nghĩa vào danh sách
        words.append((word, word_means_text, word_ipa_text))

        # Kiểm tra xem đã đủ 5 từ chưa
        if len(words) >= 5:
            # Tạo trang mới với bảng 5xN
            return render_template('result.html', words=words)
        
        return render_template('index.html', word_means=word_means_text, word_ipa=word_ipa_text)

    # Khởi tạo danh sách từ
    words = []
    
    return render_template('index.html')

@app.route('/view-table')
def view_table():
    return render_template('view_table.html', words=words)

if __name__ == '__main__':
    app.run(debug=True)
