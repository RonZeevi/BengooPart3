from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from utilities.db.db_connector import *

# about blueprint definition
changepassword = Blueprint(
    'changepassword',
    __name__,
    static_folder='static',
    static_url_path='/changepassword',
    template_folder='templates',
    url_prefix='/profile'  # הוספת prefix לכל הנתיבים בבלופרינט
)


# Routes
@changepassword.route('/changepassword')
def index():
    # בדיקה אם המשתמש מחובר
    if not session.get('logged_in'):
        return redirect(url_for('homepage.index'))
    
    return render_template('changepassword.html')


@changepassword.route('/api/change-password', methods=['POST'])
def change_password():
    # בדיקה אם המשתמש מחובר
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'User not logged in'}), 401
    
    # קבלת הנתונים מהבקשה
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    # בדיקה שכל השדות הנדרשים קיימים
    if not current_password or not new_password:
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    
    # קבלת פרטי המשתמש מהדאטה בייס
    username = session.get('username')
    user = get_user_by_username(username)
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # בדיקה שהסיסמה הנוכחית נכונה
    if user['password'] != current_password:
        return jsonify({'success': False, 'error': 'Current password is incorrect'}), 400
    
    # עדכון הסיסמה בדאטה בייס
    success = update_user_password(username, new_password)
    
    if success:
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    else:
        return jsonify({'success': False, 'error': 'Failed to update password'}), 500

