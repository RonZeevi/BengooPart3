from flask import Blueprint, render_template, session, redirect, url_for


# homepage blueprint definition
homepage = Blueprint(
    'homepage',
    __name__,
    static_folder='static',
    static_url_path='/homepage',
    template_folder='templates'
)


# Routes
@homepage.route('/')
def index():
    return render_template('homepage.html')


@homepage.route('/select_role/<role>')
def select_role(role):
    session['selected_role'] = role
    return redirect(url_for('homepage.index'))


@homepage.route('/homepage')
@homepage.route('/home')
def redirect_homepage():
    # print('I am in /Homepage route!')
    return redirect(url_for('homepage.index'))
