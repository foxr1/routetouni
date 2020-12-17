from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    name = request.form.get('name')

    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return 'Logout'
