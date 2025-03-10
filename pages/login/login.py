from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from datetime import datetime
from utilities.db.db_connector import *

# about blueprint definition
login = Blueprint(
    'login',
    __name__,
    static_folder='static',
    static_url_path='/login',
    template_folder='templates'
)


@login.route('/login', methods=['GET', 'POST'])
def index():
    # if user is already logged in and try to login again
    if session.get('logged_in') and request.method == 'GET':
        print("User already logged in, redirecting to homepage")  
        return redirect('/homepage')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt - Username: {username}")  # debug print
        
        # check if the request is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # check if the user exists in the database
        user = check_login(username, password)
        
        if user:
            # set the session 
            session.permanent = True
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = str(user.get('_id'))  
            session['role'] = user.get('role')  
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # הדפסת דיבאג
            print(f"User logged in. Session: {session}")
            
            if is_ajax:
                return jsonify({"success": True, "redirect": url_for('selectcourse.index')})
            else:
                return redirect(url_for('selectcourse.index'))
        else:
            # if the login failed
            print("Login failed - Invalid credentials")
            error_message = "Username or password is incorrect"
            
            if is_ajax:
                return jsonify({"success": False, "error": error_message})
            else:
                # if the request is not an AJAX request, return the page with the error message
                return render_template('login.html', error=error_message)
    
    return render_template('login.html')


@login.route('/signout')
def logout_func():
    session['username'] = None
    session['logged_in'] = False
    session['user_id'] = None  
    session['role'] = None  
    return redirect('/')


@login.route('/check-user', methods=['POST'])
def check_user():
    """Check if user exists in the system and retrieve their email"""
    data = request.json
    username = data.get('username')
    
    # בדיקה אם המשתמש קיים בדאטה בייס
    user = users_col.find_one({'username': username})
    
    if user:
        # אם המשתמש נמצא, החזר את המייל שלו
        return jsonify({
            'exists': True,
            'email': user.get('email', 'unknown@email.com')  # שימוש בערך ברירת מחדל אם אין מייל
        })
    else:
        # אם המשתמש לא נמצא
        return jsonify({
            'exists': False
        })

@login.route('/reset-password', methods=['POST'])
def reset_password():
    """Handle password reset request"""
    data = request.json
    username = data.get('username')
    
    # בדיקה אם המשתמש קיים
    user = users_col.find_one({'username': username})
    
    if user:
        # כאן היית מוסיף קוד לשליחת מייל אמיתי
        # אבל כרגע אנחנו רק מחזירים הצלחה
        pass
    
    # תמיד החזר הצלחה כדי לא לחשוף מידע על קיום משתמשים
    return jsonify({'success': True})


