import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def read_articles():
    try:
        with open('articles.json', 'r', encoding='utf-8') as file:
            articles = json.load(file)
    except FileNotFoundError:
        articles = []
    return articles

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home', methods=["GET"])
def home():
    articles = read_articles()
    return render_template('home.html', articles=articles)


@app.route('/article/<int:article_id>', methods=["GET"])
def article(article_id):
    articles = read_articles()
    selected_article = next(
        (article for article in articles if article["id"] == article_id),
        None,
    )
    
    if selected_article is None:
        return "Article not found", 404

    return render_template('article.html', article=selected_article)