from flask import render_template, Response, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.utils.video_stream import generate_frames
from app.admin.models import Event
from app import db

@bp.route('/')
def home():
    return render_template('main/home.html')

@bp.route('/live')
@login_required
def live():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.timestamp.desc()).all()
    return render_template('main/live.html', title='Live', events=events)

@bp.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', title='Профиль', user=current_user)
