from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_collection.forms import UserLoginForm, UserSignupForm
from marvel_collection.models import User, db, check_password_hash

from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            own_hero_name = form.own_hero_name.data
            password = form.password.data
            print(email, first_name, last_name, own_hero_name, password)

            user = User(email, first_name = first_name, last_name = last_name, own_hero_name = own_hero_name, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully become a part of the Marvel Universe, {own_hero_name}!', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please double check your input data.')

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You have successfully entered the Marvel Universe.', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Please double check your credentials as your email or password are incorrect.', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invaled Form Data: Pleace check your inputs.')
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

