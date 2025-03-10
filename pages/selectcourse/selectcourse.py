from flask import Blueprint, render_template, session, redirect, url_for
from utilities.db.db_connector import *

# about blueprint definition
selectcourse = Blueprint(
    'selectcourse',
    __name__,
    static_folder='static',
    static_url_path='/selectcourse',
    template_folder='templates'
)


# Routes
@selectcourse.route('/selectcourse')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login.index'))
    
    # קבלת שם המשתמש מהסשן
    username = session.get('username', '')
    
    # משיכת המשתמש מהדאטה בייס
    user = get_user_by_username(username)
    
    # אם המשתמש נמצא ויש לו שם מלא, השתמש בשם הפרטי שלו
    # אחרת השתמש במילה "user"
    if user and 'fullname' in user and user['fullname'].strip():
        first_name = user['fullname'].split()[0] if ' ' in user['fullname'] else user['fullname']
    else:
        first_name = "user"
    
    # שליפת נתוני הקורסים של המשתמש
    courses_data = get_user_courses_data(username)

    # העברת הנתונים לתבנית
    return render_template('selectcourse.html', 
                          first_name=first_name, 
                          courses=courses_data)
