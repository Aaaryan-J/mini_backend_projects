import json
from datetime import timedelta
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)
app.secret_key = "testingKey"
app.permanent_session_lifetime = timedelta(minutes=5)
csrf = CSRFProtect(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secret"

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


def read_articles():
    try:
        with open('articles.json', 'r', encoding='utf-8') as file:
            articles = json.load(file)
    except FileNotFoundError:
        articles = []
    except json.JSONDecodeError as error:
        raise RuntimeError("articles.json contains invalid JSON.") from error
    return articles

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session.permanent = True
            session["username"] = username
            return redirect(url_for("admin"))

        flash("Invalid username or password.", "error")
        return render_template("login.html", error="Invalid username or password.")

    if "username" in session:
        return redirect(url_for("admin"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
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

@app.route('/admin', methods=["GET", "POST"])
@admin_required
def admin():
    return render_template("admin.html", articles=read_articles())


@app.route("/new", methods=["GET", "POST"])
@admin_required
def new_article():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date = request.form.get("date", "").strip()
        content = request.form.get("content", "").strip()
        articles = read_articles()
        if not title or not date or not content:
            return render_template(
                "new_article.html",
                error="All fields are required.",
            ), 400

        new_id = max(
            (article["id"] for article in articles),
            default=0,
        ) + 1
        new_article = {
            "id": new_id,
            "title": title,
            "date_published": date,
            "content": content,
        }
        
        articles.append(new_article)

        try:
            with open('articles.json', 'w', encoding='utf-8') as file:
                json.dump(articles, file, indent=2)
        except FileNotFoundError:
            return "File not found", 404

        flash("Article created successfully.", "success")
        return redirect(url_for("admin"))
    
    return render_template("new_article.html")


@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
@admin_required
def update_article(article_id):
    articles = read_articles()
    article_index = next(
        (
            index
            for index, article in enumerate(articles)
            if article["id"] == article_id
        ),
        None,
    )

    if article_index is None:
        return "Article not found", 404

    selected_article = articles[article_index]

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date_published = request.form.get("date", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not date_published or not content:
            return render_template(
                "update_article.html",
                article=selected_article,
                error="All fields are required.",
            ), 400

        articles[article_index] = {
            "id": selected_article["id"],
            "title": title,
            "date_published": date_published,
            "content": content,
        }
        
        try:
            with open("articles.json", "w", encoding="utf-8") as file:
                json.dump(articles, file, indent=2)
        except FileNotFoundError:
            return "File not found", 404

        flash("Article updated successfully.", "success")
        return redirect(url_for("admin"))

    return render_template(
        "update_article.html",
        article=selected_article,
    )

@app.route("/delete/<int:article_id>", methods=["POST"])
@admin_required
def delete_article(article_id):
    articles = read_articles()

    remaining_articles = [
        article for article in articles if article["id"] != article_id
    ]

    if len(remaining_articles) == len(articles):
        return "Article not found", 404

    try:
        with open('articles.json', 'w', encoding='utf-8') as file:
            json.dump(remaining_articles, file, indent=2)
    except FileNotFoundError:
        return "File not found", 404

    flash("Article deleted successfully.", "success")
    return redirect(url_for("admin"))