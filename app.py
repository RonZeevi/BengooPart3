from flask import Flask, session, request, redirect, url_for, render_template, flash
from flask import redirect
from datetime import timedelta


###### App setup
app = Flask(__name__)
app.secret_key = '123'
app.permanent_session_lifetime = timedelta(minutes=15)
app.config.from_pyfile('settings.py')

###### Pages
## Homepage
from pages.homepage.homepage import homepage

app.register_blueprint(homepage)

## Login
from pages.login.login import login

app.register_blueprint(login)

## Signup
from pages.signup.signup import signup

app.register_blueprint(signup)

## SelectCourse
from pages.selectcourse.selectcourse import selectcourse

app.register_blueprint(selectcourse)

## Chat
from pages.chat.chat import chat

app.register_blueprint(chat)

## Page error handlers
from pages.page_error_handlers.page_error_handlers import page_error_handlers

app.register_blueprint(page_error_handlers)

## About us
from pages.aboutus.aboutus import aboutus

app.register_blueprint(aboutus)

## Profile
from pages.profile.profile import profile

app.register_blueprint(profile)

## changepassword
from pages.changepassword.changepassword import changepassword

app.register_blueprint(changepassword)

## Course Access
from pages.courseaccess.courseaccess import courseaccess

app.register_blueprint(courseaccess, url_prefix='/courseaccess')

###### Components
## footer
from components.footer.footer import footer

app.register_blueprint(footer)

## navigationbar
from components.navigationbar.navigationbar import navigationbar

app.register_blueprint(navigationbar)
