from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from models import User, Article

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Home OK"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user)
                return redirect(url_for("dashboard"))

            return "Invalid credentials"

        return """
        <form method="POST">
            <input name="username" placeholder="username">
            <input name="password" placeholder="password">
            <button>Login</button>
        </form>
        """

    @app.route("/dashboard")
    @login_required
    def dashboard():
        articles = Article.query.filter_by(author_id=current_user.id).all()
        return f"Dashboard OK | Articles: {len(articles)}"

    @app.route("/new-article", methods=["GET", "POST"])
    @login_required
    def new_article():
        if request.method == "POST":
            article = Article(
                title=request.form.get("title"),
                content=request.form.get("content"),
                author_id=current_user.id
            )
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("dashboard"))

        return """
        <form method="POST">
            <input name="title" placeholder="title">
            <textarea name="content"></textarea>
            <button>Publish</button>
        </form>
        """

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/create-user")
    def create_user():
        user = User(username="admin", password="admin")
        db.session.add(user)
        db.session.commit()
        return "User created"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
