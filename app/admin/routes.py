from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.admin import bp
from app.admin.forms import EventForm
from app.admin.models import Event
from app import db


@bp.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if not current_user.is_admin:
        flash('У вас нет прав доступа к этой странице', 'danger')
        return redirect(url_for('main.live'))

    form = EventForm()
    if form.validate_on_submit():
        event = Event(name=form.name.data, user_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        flash('Событие успешно добавлено!', 'success')
        return redirect(url_for('admin.add_event'))

    return render_template('admin/add_event.html', title='Добавить событие', form=form)
