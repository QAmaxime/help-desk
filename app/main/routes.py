from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import main
from ..models import Admin

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
def admin_home():
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.user_home'))
    return render_template('admin_home.html')

@main.route('/user')
def user_home():
    return render_template('user_home.html')