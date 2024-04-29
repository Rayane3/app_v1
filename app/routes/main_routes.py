from flask import Blueprint, render_template
from ..forms import LoginForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    form = LoginForm()
    return render_template('home.html', login_form=form)


