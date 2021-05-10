from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import random
from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, ConfirmForm
from ..models import User
from flask_mail import Message
from flask_mail import Mail
from .. import mail

users = Blueprint('users', __name__,  static_folder='static', template_folder='templates')
# mail = Mail(app)
""" ************ User Management views ************ """


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("stocks.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        num = random.randint(1111,9999)
        user = User(username=form.username.data, email=form.email.data, password=hashed, confirmed = False, code = num)
        user.save()
        msg = f'Hello, here is your validation code: {num}'
        msg = Message(msg,sender="skillguy321@gmail.com", recipients=[form.email.data])
        mail.send(msg)
        print('a')
        return redirect(url_for("users.confirm"))

    return render_template("register.html", title="Register", form=form)

@users.route("/confirm", methods=["GET", "POST"])
def confirm():
    if current_user.is_authenticated:
        return redirect(url_for("stocks.index"))
    form = ConfirmForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        # temp_code = User.objects(code = )
        # print(user['code'])
        if(user['code'] == form.code.data):
            print('a')
            user['confirmed'] = True
            user.save()
            return redirect(url_for("users.login"))
    return render_template("confirm.html", title="Confirm", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("stocks.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and user['confirmed'] == False:
            flash("Make sure to confirm your code from your email")
        if user is not None and user['confirmed'] == True and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("stocks.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )

