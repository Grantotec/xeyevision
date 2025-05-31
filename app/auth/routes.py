from flask import render_template, redirect, url_for, flash, request
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User
from app import db, login_manager
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.live'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            gender=form.gender.data,
            birth_date=form.birth_date.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.live'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.live'))
        else:
            flash('Неверный email или пароль. Пожалуйста, попробуйте снова.', 'danger')

    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
