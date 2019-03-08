from bottle import (
    route, run, template, request, redirect
)
import string
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import bottle
import os
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id = request.query.id
    s = session()
    rows = s.query(News).filter(News.id == id).update({'label': label})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news('https://news.ycombinator.com/newest', 3)
    for news in news_list:
        if s.query(News).filter(News.author == news['author'],
                                News.title == news['title']).first() is not None:
            print('lol')
            continue
        else:
            news = News(title=news.get('title'),
                        author=news.get('author'),
                        url=news.get('url'),
                        comments=news.get('comments'),
                        points=news.get('points'))
            s.add(news)
            s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        [prediction] = classifier.predict([clean(row.title)])
        if prediction == 'good':
            good.append(row)
        elif prediction == 'maybe':
            maybe.append(row)
        else:
            never.append(row)

    return template('news_information', good=good, maybe=maybe, never=never)


if __name__ == "__main__":
    s = session()
    labeled_news = s.query(News).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier()
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
