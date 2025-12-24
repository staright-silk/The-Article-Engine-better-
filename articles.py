from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from models import Article
from app import db
from search import add_to_index

articles_bp = Blueprint("articles", __name__)

@articles_bp.route("/dashboard")
@login_required
def dashboard():
    articles = Article.query.filter_by(author_id=current_user.id).all()
    return render_template("dashboard.html", articles=articles)

@articles_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_article():
    if request.method == "POST":
        article = Article(
            title=request.form["title"],
            content=request.form["content"],
            author_id=current_user.id
        )
        db.session.add(article)
        db.session.commit()
        add_to_index(article)
        return redirect("/dashboard")
    return render_template("new_article.html")

@articles_bp.route("/article/<int:id>")
def view_article(id):
    article = Article.query.get_or_404(id)
    return render_template("article.html", article=article)
