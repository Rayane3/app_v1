from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from ..models import User
from ..forms import LoginForm, RegistrationForm
from .. import db
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('booking'))
            else:
                flash('Invalid password provided.', 'error')
        else:
            flash('Username does not exist.', 'error')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


