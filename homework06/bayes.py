from collections import Counter
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y."""
        lst = []
        for sentence, clss in zip(X, y):
            for word in sentence.split():
                lst.append((word, clss))
        self.words_labels = Counter(lst)
        self.counted_labels = dict(Counter(y))
        words = [word for sentence in X for word in sentence.split()]
        self.counted_words = dict(Counter(words))

        self.infomation = {
            'labels': {},
            'words': {},
        }

        for cur_label in self.counted_labels:
            params = {
                'amount_by_label': self.count_words(cur_label),
                'likelihood': self.counted_labels[cur_label] / len(y),
            }
            self.infomation['labels'][cur_label] = params
        for word in self.counted_words:
            params = {}
            for cur_label in self.counted_labels:
                params[cur_label] = self.smoothing(word, cur_label)
            self.infomation['words'][word] = params

    def predict(self, X):
        """ Perform labelification on an array of test vectors X. """
        answers_lst = []
        for sentence in X:
            words = sentence.split()
            likely_labels = []
            for cur_label in self.infomation['labels']:
                likelihood = self.infomation['labels'][cur_label]['likelihood']
                total_score = math.log(likelihood, math.e)
                for word in words:
                    word_dict = self.infomation['words'].get(word, None)
                    if word_dict:
                        total_score += math.log(word_dict[cur_label], math.e)
                likely_labels.append((total_score, cur_label))
            _, answer = max(likely_labels)
            answers_lst.append(answer)

        return answers_lst

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        total = len(y_test)
        correct = 0
        for i, answer in enumerate(self.predict(X_test)):
            if answer == y_test[i]:
                correct += 1

        return correct / total

    def smoothing(self, word, cur_label):
        """ Returns the smoothed likelihood with the given word and label in loop. """
        nc = self.infomation['labels'][cur_label]['amount_by_label']
        nic = self.words_labels.get((word, cur_label), 0)
        d = len(self.counted_words)
        alpha = self.alpha

        return (nic + alpha) / (nc + alpha * d)

    def count_words(self, cur_label):
        """ Returns the count of words with the given label. """
        count = 0
        for word, label_name in self.words_labels:
            if cur_label == label_name:
                count += self.words_labels[(word, cur_label)]

        return count