from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from utilities.db.db_connector import *

# about blueprint definition
signup = Blueprint(
    'signup',
    __name__,
    static_folder='static',
    static_url_path='/signup',
    template_folder='templates'
)


# Routes
@signup.route('/signup/<role>')
def index(role):
    # בדיקה אם המשתמש כבר מחובר
    if session.get('logged_in'):
        # אם כן, הפנה אותו לדף הבית
        return redirect(url_for('homepage.index'))
    
    print(f"Signup role: {role}")  # debug print
    return render_template('signup.html', selected_role=role)

@signup.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # קבלת הנתונים מהטופס
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        print(f"Checking if user exists: {username}, email: {email}")
        
        # בדיקה אם המשתמש כבר קיים
        user_check = check_user_exists(email=email, username=username)
        print(f"User check result: {user_check}")  # הדפסת תוצאת הבדיקה
        
        if user_check['exists']:
            error_message = ""
            if user_check['email_exists']:
                error_message += "The email is already registered. "
            if user_check['username_exists']:
                error_message += "The username is already taken. "
            
            print(f"User exists error: {error_message}")
            
            # בדיקה אם זו בקשת AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': error_message})
            
            # אחרת, החזרת המשתמש לדף ההרשמה עם הודעת שגיאה
            try:
                flash(error_message, 'error')
            except:
                pass
            
            # החזרה לדף ההרשמה עם פרמטר שגיאה
            return redirect(url_for('signup.index', role=role, error=error_message))
        
        # יצירת מילון עם נתוני המשתמש
        user_data = {
            'fullname': fullname,
            'email': email,
            'username': username,
            'password': password,
            'role': role
        }
        
        # הוספת המשתמש למסד הנתונים
        user_id = insert_user(user_data)
        print(f"User registered with ID: {user_id}")  # הדפסת לוג
        
        # בדיקה אם זו בקשת AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True, 
                'redirect': url_for('login.index'),
                'message': 'Registration successful! Redirecting to login page...'
            })
        
        return redirect(url_for('login.index'))
