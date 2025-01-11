from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, send_file
from app import db
from app import login_manager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import qrcode
from io import BytesIO
import os
from app.models import User, Event, Ticket, CartItem
from app.forms import RegistrationForm, LoginForm, AddToCart

main = Blueprint('main', __name__)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.context_processor
def inject_user():
    return dict(current_user=current_user)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first() or User.query.filter_by(password=password).first():
            flash('Username or email already exists', 'danger')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now login', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.portal', user_id=user.id))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)

# Main application routes
@main.route('/portal', methods=['GET', 'POST'])
@login_required
def portal():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_count = len(cart_items)
    events = Event.query.all()    
    return render_template('UserPortal.html', events=events, current_user=current_user, cart_count=cart_count)


@main.route('/add_to_cart/<int:event_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(event_id):
    event = Event.query.get_or_404(event_id)
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_count = len(cart_items)
    form = AddToCart()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity > (event.total_tickets - event.tickets_sold):
            flash('Not enough tickets available', 'danger')
        else:
            cart_item = CartItem(user_id=current_user.id, event_id=event_id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()
            flash('Ticket added to cart', 'success')
        return redirect(url_for('main.view_cart'))
    return render_template('add_to_cart.html', event=event, form=form, cart_count=cart_count)



@main.route('/view_cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(int(item.event.ticket_prices) * item.quantity for item in cart_items)
    cart_count = len(cart_items)

    if request.method == 'POST':

        if 'checkout' in request.form:
            return redirect(url_for('main.view_cart'))
        
        for item in cart_items:
            quantity = request.form.get(f'quantity-{item.id}')
            if quantity:
                item.quantity = int(quantity)
        db.session.commit()
        flash('Cart updated successfully!', 'success')
        return redirect(url_for('main.view_cart'))
    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

@main.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart', 'success')
        return redirect(url_for('main.view_cart'))
    return 'Error removing from Cart', 400

@main.route('/ticket/<int:ticket_id>/qr')
@login_required
def ticket_qr(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    qr = qrcode.make(f'Ticket ID: {ticket.id}, Event: {ticket.event.title}, User: {ticket.user.username}')
    buffer = BytesIO()
    qr.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f'ticket_{ticket.id}.png')


@main.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    for item in cart_items:
        event = Event.query.get_or_404(item.event_id)
        if item.quantity > (event.total_tickets - event.tickets_sold):
            flash('Not enough tickets available', 'danger')
            return redirect(url_for('main.view_cart', current_user=current_user.id))
        event.tickets_sold += item.quantity
        event.total_tickets -= item.quantity


        for _ in range(item.quantity):
            ticket = Ticket(user_id=current_user.id, event_id=item.event_id, quantity=item.quantity)
            db.session.add(ticket)
        db.session.delete(item)
    db.session.commit()
    flash('Purchase successful! Tickets have been added to your account', 'success')
    return redirect(url_for('main.my_tickets'))

@main.route('/event_info/<int:event_id>')
@login_required
def event_info(event_id):
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_count = len(cart_items)
    event = Event.query.get_or_404(event_id)
    return render_template('event_info.html', event=event, cart_count=cart_count)


@main.route('/my_tickets')
@login_required
def my_tickets():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_count = len(cart_items)
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('my_tickets.html', tickets=tickets, cart_count=cart_count)

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('main.login'))


    