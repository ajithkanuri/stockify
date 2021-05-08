from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import stock_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

stocks = Blueprint('stocks', __name__, static_folder='static', template_folder='templates')

@stocks.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("stocks.stock_detail", symbol=form.search_query.data))

    return render_template("index.html", form=form)


@stocks.route("/stock/<symbol>", methods=["GET", "POST"])
def stock_detail(symbol):
    try:
        result = stock_client.search(symbol)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = MovieReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=symbol,
            movie_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=symbol)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


@stocks.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)