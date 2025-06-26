from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Ticket, User
from ..forms import TicketForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_home():
    if not current_user.is_admin():
        return redirect(url_for('main.user_home'))
    all_tickets = Ticket.query.all()
    my_tickets = Ticket.query.filter_by(assignee_id=current_user.id).all()
    admins = User.query.filter_by(role='admin').all()
    return render_template('admin_home.html', all_tickets=all_tickets, my_tickets=my_tickets, admins=admins)

@main.route('/user')
@login_required
def user_home():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('user_home.html', tickets=tickets)

@main.route('/update-ticket/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    form = TicketForm()
    if not current_user.is_admin():
        return redirect(url_for('main.user_home'))

    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')
    new_assignee = request.form.get('assignee')

    if new_status:
        ticket.status = new_status
    if new_assignee:
        ticket.assignee_id = int(new_assignee)

    db.session.commit()
    flash('Ticket updated.', 'success')
    return redirect(url_for('main.admin_home'))

@main.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('main.admin_home'))

@main.route('/submit-ticket', methods=['GET','POST'])
@login_required
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data, user_id=current_user.id, system=form.system.data, system_type=form.system_type.data)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted.', 'success')
        return redirect(url_for('main.user_home'))
    return render_template('submit_ticket.html', form=form)