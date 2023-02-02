from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login.utils import login_required
from app import db
from app.model.models import Student
from app.controller.auth_forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user
from config import Config

auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()

    if rform.validate_on_submit():
        student = Student(username=rform.username.data, firstname=rform.firstname.data, lastname=rform.lastname.data, email=rform.email.data, address=rform.address.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Registration successful.')

    return render_template('register.html', form = rform)

@auth_blueprint.route('/login', methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    lform = LoginForm()

    if lform.validate_on_submit():
        student = Student.query.filter_by(username = lform.username.data).first()

        if (student is None) or (student.check_password(lform.password.data) == False):
            flash('Invalid username or password') 
            return redirect(url_for('auth.login'))

        login_user(student, lform.remember_me.data)

        return redirect(url_for('routes.index'))
        
    return render_template('login.html', title='Sign In', form=lform)

@auth_blueprint.route('/logout', methods=['GET'])   
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))