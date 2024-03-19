from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html', title="Home")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.username.data
        pw = form.password.data

        flash(f"Логин {uname};{pw}", "success")
        return redirect(url_for('login'))
    return render_template('login.html', form=form, title="Вход")