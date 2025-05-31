from flask import render_template, redirect, url_for, flash, request
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User
from app import db
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash  # Добавлен check_password_hash


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.live'))  # Исправлен url_for

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
        return redirect(url_for('auth.login'))  # Исправлен url_for

    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.live'))  # Исправлен url_for

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Исправлена проверка пароля
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # Добавлен remember
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.live'))  # Исправлен url_for
        else:
            flash('Неверный email или пароль. Пожалуйста, попробуйте снова.', 'danger')

    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/logout')
@login_required  # Добавлен декоратор защиты
def logout():
    logout_user()
    return redirect(url_for('main.home'))  # Исправлен url_for