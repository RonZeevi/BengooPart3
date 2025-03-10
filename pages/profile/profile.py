from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from utilities.db.db_connector import *
from bson import ObjectId

profile = Blueprint(
    'profile',
    __name__,
    static_folder='static',
    static_url_path='/profile',
    template_folder='templates'
)

# פונקציה עזר לשליפת קורס לפי שמו
def get_course_by_name(course_name):
    return courses_col.find_one({"course_name": course_name})

@profile.route('/')
def redirect_to_profile():
    return redirect(url_for('profile.index'))

@profile.route('/profile')
def index():
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return redirect(url_for('login.index'))
    
    # הפניה לדף הפרופיל עם שם המשתמש
    username = session.get('username')
    return redirect(url_for('profile.user_profile', username=username))

@profile.route('/profile/<username>')
def user_profile(username):
    # בדיקה אם המשתמש מחובר
    if not session.get('user_id'):
        return redirect(url_for('login.index'))
    
    # שליפת נתוני המשתמש המחובר
    logged_in_username = session.get('username')
    
    # בדיקה אם המשתמש מנסה לגשת לפרופיל של משתמש אחר
    if username != logged_in_username:
        return redirect(url_for('profile.user_profile', username=logged_in_username))
    
    # שליפת נתוני המשתמש מה-MongoDB לפי ה-username
    print(f"Looking for user with username: {username}")
    
    user = get_user_by_username(username)
    
    if not user:
        # אם המשתמש לא נמצא, החזר לדף ההתחברות
        print(f"User with username {username} not found")
        session.clear()
        return redirect(url_for('login.index'))
    
    # הכנת אובייקט המשתמש לתצוגה
    user_data = {
        'username': user.get('username', ''),
        'fullname': user.get('fullname', ''),
        'email': user.get('email', ''),
    }
    
    # שליפת נתוני הקורסים של המשתמש
    courses_data = get_user_courses_data(username)
    
    # הדפסת מידע לצורכי דיבוג
    print(f"Rendering profile with user: {user_data}")
    print(f"Courses data: {courses_data}")
    
    # העברת הנתונים לתבנית
    return render_template('profile.html', 
                          user=user_data, 
                          courses=courses_data)

@profile.route('/course-access/<course_id>')
def course_access(course_id):
    # הדפסת דיבוג
    print(f"Redirecting to courseaccess with course_id: {course_id}")
    
    # הפניה ישירה לנתיב במקום להשתמש ב-url_for
    return redirect(f'/courseaccess/{course_id}')

@profile.route('/api/course-access/add', methods=['POST'])
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
    
    # בדיקה אם המשתמש שרוצים להוסיף קיים
    user_to_add = get_user_by_username(username_to_add)
    
    if not user_to_add:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # הוספת הקורס למשתמש
    success = add_user_to_course(username_to_add, course.get('course_name'))
    
    if success:
        return jsonify({
            "success": True, 
            "message": f"User {username_to_add} added to course {course.get('course_name')}"
        })
    else:
        return jsonify({"success": False, "message": "User already enrolled"}), 400

@profile.route('/api/course-access/remove', methods=['POST'])
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
