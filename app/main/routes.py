from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Ticket, Admin
from ..forms import TicketForm

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
@login_required
def user_home():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('user_home.html', tickets=tickets)

@main.route('/submit-ticket', methods=['GET','POST'])
@login_required
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted.', 'success')
        return redirect(url_for('main.user_home'))
    return render_template('submit_ticket.html', form=form)