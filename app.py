from flask import Flask, request, render_template
from spell_checker import SpellChecker

app = Flask(__name__)

s = SpellChecker()

@app.route('/', methods=['GET', 'POST'])
def main():
    spell_checked_message = None
    spell_checked_word = None
    if request.method == 'POST':
        if request.form['button'] == "Spell Check Word":
            word = request.form['word']
            spell_checked_word = s.suggested_words(word)
        else:
            text = request.form['text']
            spell_checked_message = s.spell_check_message(text)
    return render_template("index.html", message=spell_checked_message, word=spell_checked_word)

if __name__ == '__main__':
    app.run()
