import string
import random
import re

class SpellChecker(object):
    def __init__(self, dict_file='sowpods.txt', freq_file='word_frequences.csv'):
        with open(dict_file) as f:
            self.dictionary = f.read().lower().split()
        with open('word_frequencies.csv') as f:
            f = f.read().split('\n')
            self.frequencies = {}
            for row in f:
                word, freq = row.split(',')
                self.frequencies[word] = freq
        for word in self.dictionary:
            if word not in self.frequencies:
                self.frequencies[word] = '1'

    def spell_check_message(self, message):
        words = re.findall("\w+'*\w+", message)
        for word in words:
            correct, correct_spelling = self.spell_check(word)
            if not correct:
                message = message.replace(word, correct_spelling)
        return message

    def spell_check(self, word):
        if word in self.dictionary:
            return True, word
        elif "'" in word:
            return True, word
        else:
            pos_words = list(self.get_pos_words(word))
            if pos_words:
                frequent_words = [(word, self.frequencies[word]) for word in pos_words \
                                  if word in self.frequencies]
                correct_word = max(frequent_words, key=lambda x: int(x[1]))[0] \
                               if frequent_words else word
            else:
                correct_word = word

            return False, correct_word

    def get_pos_words(self, word, steps=1):
        if steps == 0: return []
        words = []
        splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
        for first, last in splits:
            inserts = [first + i + last for i in string.lowercase]
            transpose = [first[:-1] + last[0] + first[-1] + last[1:]] \
                        if last and first else []
            replace = [first[:-1] + i + last for i in string.lowercase if first]
            delete = [first[:-1] + last] if first else []
            [words.extend(edit) for edit in [inserts, transpose, \
                                             replace, delete]]
        for word in set(words):
            words.extend(self.get_pos_words(word, steps-1))
        return set(words)

def test():
    s = SpellChecker()
    incorrect_words = []
    with open("spelldata.csv") as f:
        f = f.read().split()
        for row in f:
            words = row.split(",")
            incorrect_words.append(words)
    num_correct = 0.0
    num_incorrect = 0
    for correct, word in incorrect_words:
        if not s.spell_check(word) == (False, correct):
            num_incorrect += 1
        else:
            num_correct += 1
        print num_correct + num_incorrect
    print num_correct / (num_correct+num_incorrect)
    correct_words = []
    for word in correct_words:
        assert s.spell_check(word) == (True, word)

if __name__ == '__main__':
    test()
