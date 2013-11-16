import string
import random
import re

class SpellChecker(object):
    def __init__(self, dict_file='sowpods.txt', freq_file='combined_freqs.csv'):
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
            correct, correct_spelling = self.spell_check(word, autocorrect=True)
            if not correct:
                message = message.replace(word, correct_spelling)
        return message

    def spell_check(self, word, autocorrect=False):
        if word in self.dictionary:
            return True, word
        # don't check words with punctuation
        elif re.search("\W", word):
            return False, word
        else:
            pos_words = list(self.get_pos_words(word))
            frequent_words = [(w, self.frequencies[w]) for w in pos_words \
                              if w in self.frequencies]
            sorted_words = sorted(frequent_words, key=lambda x: int(x[1]), reverse=True)
            if not sorted_words:
                return False, word
            if autocorrect:
                correct_word = sorted_words[0][0]
                return False, correct_word
            return False, sorted_words

    def suggested_words(self, word):
        correct, pos_words = self.spell_check(word)
        if correct:
            return "%s is a valid word" % word
        elif pos_words == word:
            return "There were no word suggestions for %s" % word
        else:
            return "Suggestions for %s: %s" % (word, ", ".join(word[0] for word in pos_words))

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
        if not s.spell_check(word, autocorrect=True) == (False, correct):
            num_incorrect += 1
        else:
            num_correct += 1
        print s.suggested_words(word)
        print num_correct + num_incorrect
    print num_correct / (num_correct+num_incorrect)
    correct_words = []
    for word in correct_words:
        assert s.spell_check(word) == (True, word)

if __name__ == '__main__':
    test()
