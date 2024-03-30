from app import app
from flask import render_template, url_for, redirect, flash, send_from_directory, request, abort
from app.forms import LoginForm, RegisterForm
from app.models import User
import os
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db


@app.route('/favicon.ico', methods=['GET','POST'])
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'), 'logo.png')



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html', title="Home")


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        flash("Успешный вход", "success")
        return redirect(next_page)
    return render_template('login.html', form=form, title="Вход")


@app.route('/regiser', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Вы уже зарегистрированы! Выйдите из системы для регистрации.', 'warning')
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_passwrod(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Успешная регистрация. Ваш ID {user.id}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/lk')
#@login_required
def lk():
    if current_user.is_anonymous:
        abort(403)
    return render_template('lk.html', title='ЛК')

@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'warning')
    return redirect(url_for('index'))