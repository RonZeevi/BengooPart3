from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from utilities.db.db_connector import *
import urllib.parse

courseaccess = Blueprint(
    'courseaccess',
    __name__,
    static_folder='static',
    static_url_path='/courseaccess',
    template_folder='templates'
)

@courseaccess.route('/<course_id>')
def course_access(course_id):
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return redirect(url_for('login.index'))
    
    # שליפת נתוני המשתמש
    username = session.get('username')
    user = get_user_by_username(username)
    
    if not user:
        return redirect(url_for('login.index'))
    
    # שליפת נתוני הקורס
    try:
        course = get_course_by_id(course_id)
    except:
        return redirect(url_for('profile.user_profile', username=username))
    
    if not course:
        return redirect(url_for('profile.user_profile', username=username))
    
    # בדיקה אם המשתמש הוא המרצה של הקורס
    if course.get('lecturer') != user.get('fullname'):
        return redirect(url_for('profile.user_profile', username=username))
    
    # שליפת רשימת המשתמשים שיש להם גישה לקורס
    users_with_access = get_users_with_access_to_course(course.get('course_name'))
    
    course_users = []
    for user_with_access in users_with_access:
        course_users.append({
            'username': user_with_access.get('username'),
            'fullname': user_with_access.get('fullname'),
            'email': user_with_access.get('email')
        })
    
    return render_template('courseaccess.html', 
                          course=course,
                          course_users=course_users)

@courseaccess.route('/api/add', methods=['POST'])
def add_user_to_course_api():
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    # קבלת נתונים מהבקשה
    data = request.json
    course_id = data.get('course_id')
    username_to_add = data.get('username')
    
    # בדיקת תקינות הנתונים
    if not course_id or not username_to_add:
        return jsonify({"success": False, "message": "Missing data"}), 400
    
    # שליפת נתוני המשתמש המחובר
    current_username = session.get('username')
    current_user = get_user_by_username(current_username)
    
    # שליפת נתוני הקורס
    course = get_course_by_id(course_id)
    
    if not course:
        return jsonify({"success": False, "message": "Course not found"}), 404
    
    # בדיקה אם המשתמש המחובר הוא המרצה של הקורס
    if course.get('lecturer') != current_user.get('fullname'):
        return jsonify({"success": False, "message": "Not authorized"}), 403
    
    # הוספת הקורס למשתמש
    success = add_user_to_course(username_to_add, course.get('course_name'))
    
    if success:
        return jsonify({
            "success": True, 
            "message": f"User {username_to_add} added to course {course.get('course_name')}"
        })
    else:
        return jsonify({"success": False, "message": "User already enrolled or not found"}), 400

@courseaccess.route('/api/remove', methods=['POST'])
def remove_user_from_course_api():
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    # קבלת נתונים מהבקשה
    data = request.json
    course_id = data.get('course_id')
    username_to_remove = data.get('username')
    
    # בדיקת תקינות הנתונים
    if not course_id or not username_to_remove:
        return jsonify({"success": False, "message": "Missing data"}), 400
    
    # שליפת נתוני המשתמש המחובר
    current_username = session.get('username')
    current_user = get_user_by_username(current_username)
    
    # שליפת נתוני הקורס
    course = get_course_by_id(course_id)
    
    if not course:
        return jsonify({"success": False, "message": "Course not found"}), 404
    
    # בדיקה אם המשתמש המחובר הוא המרצה של הקורס
    if course.get('lecturer') != current_user.get('fullname'):
        return jsonify({"success": False, "message": "Not authorized"}), 403
    
    # הסרת הקורס מהמשתמש
    success = remove_user_from_course(username_to_remove, course.get('course_name'))
    
    if success:
        return jsonify({
            "success": True, 
            "message": f"User {username_to_remove} removed from course {course.get('course_name')}"
        })
    else:
        return jsonify({"success": False, "message": "User not enrolled in this course"}), 400

@courseaccess.route('/api/course/id/<course_id>')
def get_course_data(course_id):
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    # שליפת נתוני המשתמש
    username = session.get('username')
    user = get_user_by_username(username)
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # שליפת נתוני הקורס
    course = get_course_by_id(course_id)
    
    if not course:
        return jsonify({"success": False, "message": "Course not found"}), 404
    
    # בדיקה אם המשתמש הוא המרצה של הקורס
    if course.get('lecturer') != user.get('fullname'):
        return jsonify({"success": False, "message": "Not authorized"}), 403
    
    # שליפת רשימת המשתמשים שיש להם גישה לקורס
    users_with_access = get_users_with_access_to_course(course.get('course_name'))
    
    course_users = []
    for user_with_access in users_with_access:
        course_users.append({
            'username': user_with_access.get('username'),
            'fullname': user_with_access.get('fullname'),
            'email': user_with_access.get('email')
        })
    
    # המרת ObjectId ל-string
    course_data = {
        "_id": str(course.get('_id')),
        "course_name": course.get('course_name'),
        "lecturer": course.get('lecturer')
    }
    
    return jsonify({
        "success": True,
        "course": course_data,
        "course_users": course_users
    })

@courseaccess.route('/api/course/name/<course_name>')
def get_course_data_by_name(course_name):
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    # פענוח שם הקורס מה-URL - פענוח כפול במקרה הצורך
    try:
        # ניסיון לפענח פעם אחת
        decoded_course_name = urllib.parse.unquote(course_name)
        
        # בדיקה אם יש צורך בפענוח נוסף (אם עדיין יש סימני % בטקסט)
        if '%' in decoded_course_name:
            decoded_course_name = urllib.parse.unquote(decoded_course_name)
    except:
        # אם הפענוח נכשל, נשתמש בערך המקורי
        decoded_course_name = course_name
    
    # שליפת נתוני המשתמש
    username = session.get('username')
    user = get_user_by_username(username)
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # שליפת נתוני הקורס
    course = get_course_by_name(decoded_course_name)
    
    if not course:
        return jsonify({"success": False, "message": "Course not found"}), 404
    
    # בדיקה אם המשתמש הוא המרצה של הקורס
    if course.get('lecturer') != user.get('fullname'):
        return jsonify({"success": False, "message": "Not authorized"}), 403
    
    # שליפת רשימת המשתמשים שיש להם גישה לקורס
    users_with_access = get_users_with_access_to_course(decoded_course_name)
    
    course_users = []
    for user_with_access in users_with_access:
        course_users.append({
            'username': user_with_access.get('username'),
            'fullname': user_with_access.get('fullname'),
            'email': user_with_access.get('email')
        })
    
    # המרת ObjectId ל-string
    course_data = {
        "_id": str(course.get('_id')),
        "course_name": course.get('course_name'),
        "lecturer": course.get('lecturer')
    }
    
    return jsonify({
        "success": True,
        "course": course_data,
        "course_users": course_users
    })
