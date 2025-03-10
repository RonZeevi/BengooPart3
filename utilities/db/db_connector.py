import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# get your uri directly
uri = os.environ.get('DB_URI')

# create cluster
cluster = MongoClient(uri, server_api=ServerApi('1'))

# get all dbs and collections that needed
bengoo = cluster['bengoo'] 
users_col = bengoo['users']
courses_col = bengoo['courses'] 

# ---- User Functions ----

def insert_user(user_data):
    """הוספת משתמש חדש למסד הנתונים"""
    result = users_col.insert_one(user_data)
    return result

def check_user_exists(email=None, username=None):
    """בדיקה אם משתמש קיים לפי אימייל או שם משתמש"""
    result = {
        'exists': False,
        'email_exists': False,
        'username_exists': False
    }
    
    # בדיקה אם האימייל קיים
    if email:
        email_user = users_col.find_one({'email': email})
        if email_user:
            result['email_exists'] = True
            result['exists'] = True
    
    # בדיקה אם שם המשתמש קיים
    if username:
        username_user = users_col.find_one({'username': username})
        if username_user:
            result['username_exists'] = True
            result['exists'] = True
    
    return result

def check_login(username, password):
    """בדיקת התחברות משתמש"""
    user = users_col.find_one({'username': username, 'password': password})
    return user

def get_user_by_username(username):
    """שליפת משתמש לפי שם משתמש"""
    return users_col.find_one({"username": username})

def get_user_profile_image(username):
    """שליפת תמונת פרופיל של משתמש"""
    user = users_col.find_one({'username': username})
    if user and 'profile' in user:
        return user['profile']
    return None

def update_user_password(username, new_password):
    """עדכון סיסמת משתמש"""
    result = users_col.update_one(
        {'username': username},
        {'$set': {'password': new_password}}
    )
    return result.modified_count > 0

# ---- Course Functions ----

def get_course_by_name(course_name):
    """שליפת קורס לפי שם"""
    return courses_col.find_one({'course_name': course_name})

def get_course_by_id(course_id):
    """שליפת קורס לפי מזהה"""
    return courses_col.find_one({"_id": ObjectId(course_id)})

def get_all_courses():
    """שליפת כל הקורסים"""
    return list(courses_col.find())

def get_users_with_access_to_course(course_name):
    """שליפת כל המשתמשים שיש להם גישה לקורס מסוים"""
    return list(users_col.find({"courses": course_name}))

def add_user_to_course(username, course_name):
    """הוספת קורס למשתמש"""
    user = get_user_by_username(username)
    if not user:
        return False
    
    user_courses = user.get('courses', [])
    if isinstance(user_courses, str):
        user_courses = [user_courses]
    
    if course_name not in user_courses:
        user_courses.append(course_name)
        users_col.update_one(
            {"username": username},
            {"$set": {"courses": user_courses}}
        )
        return True
    return False

def remove_user_from_course(username, course_name):
    """הסרת קורס ממשתמש"""
    user = get_user_by_username(username)
    if not user:
        return False
    
    user_courses = user.get('courses', [])
    if isinstance(user_courses, str):
        user_courses = [user_courses]
    
    if course_name in user_courses:
        user_courses.remove(course_name)
        users_col.update_one(
            {"username": username},
            {"$set": {"courses": user_courses}}
        )
        return True
    return False

def get_user_courses_data(username):
    """שליפת נתוני הקורסים של משתמש"""
    user = get_user_by_username(username)
    if not user:
        return []
    
    user_courses = user.get('courses', [])
    if isinstance(user_courses, str):
        user_courses = [user_courses]
    
    courses_data = []
    for course_name in user_courses:
        course = get_course_by_name(course_name)
        if course:
            is_lecturer = False
            if course.get('lecturer') == user.get('fullname'):
                is_lecturer = True
            
            courses_data.append({
                'name': course.get('course_name', ''),
                'lecturer': course.get('lecturer', ''),
                'lecturer_title': course.get('title', ''),
                'is_lecturer': is_lecturer,
                'course_id': str(course.get('_id', ''))
            })
    
    return courses_data


