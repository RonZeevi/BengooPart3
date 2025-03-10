from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import os
import google.generativeai as genai

# about blueprint definition
chat = Blueprint(
    'chat',
    __name__,
    static_folder='static',
    static_url_path='/chat',
    template_folder='templates'
)

# הגדרת ה-API של Gemini מתוך משתנה סביבה
api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# יצירת משתנה גלובלי לשמירת היסטוריית הצ'אט
chat_sessions = {}

# Routes
@chat.route('/chat')
def index():
    # בדיקה אם המשתמש מחובר
    if not session.get('logged_in'):
        return redirect(url_for('login.index'))
    
    # קבלת שם הקורס מהפרמטר בכתובת
    course_name = request.args.get('course', 'Together')
    
    # העברת שם הקורס לתבנית
    return render_template('chat.html', course_name=course_name)

@chat.route('/send_message', methods=['POST'])
def send_message():
    if not session.get('logged_in'):
        return jsonify({'error': 'User not logged in'}), 401
    
    user_message = request.json.get('message')
    user_id = session.get('username', 'default_user')
    
    # יצירת או קבלת סשן צ'אט קיים
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    try:
        response = chat_sessions[user_id].send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
