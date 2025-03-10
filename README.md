# BENGOO 

## Project Description
בנגו היא פלטפורמה שמשלבת טכנולוגיית בינה מלאכותית עם כלים ללמידה אקדמית. המערכת מאפשרת לסטודנטים ולמרצים לנהל קורסים, לשתף מידע ולהשתמש בצ'אט חכם המבוסס על Gemini API לצורך סיוע בלימודים.

## Key Features
- **Permission System**: Separation between users by roles (student/lecturer)
- **Course Management**: Creation, editing, and access allocation to courses
- **AI Chat**: Integration with Gemini API for answers to academic questions
- **Intuitive User Interface**: Clean and user-friendly design

## Current Limitations
- No custom prompts available yet
- Password recovery functionality not implemented
- Chat response may be slow due to using the free version of Gemini API
- Chat history is not saved between sessions

## Future Features
- File Upload and Processing: We plan to implement file upload capabilities and AI-powered analysis
- Speech-to-Text Conversion: Future versions will include converting lecture recordings to text for easier access and analysis
- Due to time constraints, the current development is focused on core functionalities only, while these advanced features are planned for future releases
- Profile pictures - It will be possible to upload profile pictures as part of the registration process. 

## Website Flow

### For New Users:
1. Enter the homepage
2. Choose a role (student/lecturer)
3. Register to the system
4. Log in to the system
5. Select a course from the course list
6. Use the AI chat for course-related questions

### For Lecturers:
1. Log in to the system
2. Enter your profile section by clicking on the profile picture
3. Manage course access (add/remove students)
4. Use the AI chat for teaching support

## Screenshots and Page Descriptions

### Homepage
<img width="947" alt="image" src="https://github.com/user-attachments/assets/1d92bb38-bc6b-49ec-ba4e-e17ad8e8beb2" />
The homepage displays the system logo and allows role selection and registration/login.

### Registration Page
![Registration Page](static/media/img/screenshots/signup.png)
Registration page with fields for personal information and role selection.

### Login Page
![Login Page](static/media/img/screenshots/login.png)
Login page for registered users.

### User Profile
![User Profile](static/media/img/screenshots/profile.png)
The profile page displays user details and their course list.

### Course Selection
![Course Selection](static/media/img/screenshots/selectcourse.png)
Page for selecting a course from the list of courses available to the user.

### Course Access Management
![Course Access Management](static/media/img/screenshots/courseaccess.png)
Page that allows lecturers to manage course access (add/remove students).

### AI Chat
![AI Chat](static/media/img/screenshots/chat.png)
Smart chat interface based on Gemini API for course-related questions and answers.

### Change Password
![Change Password](static/media/img/screenshots/changepassword.png)
Page for changing the user's password.

### About
![About](static/media/img/screenshots/aboutus.png)
Page displaying information about the developers and the project.

## Installation and Operation Instructions

### Prerequisites:
1. Python 3.8 or higher
2. MongoDB
3. Gemini API key

### Installation:
1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables in .env file:
   ```
   DB_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
   GEMINI_API_KEY="your-gemini-api-key"
   ```

3. Run the server:
   ```
   flask run
   ```

4. Access the website at:
   ```
   http://localhost:5000
   ```

## Technologies
- **Server-side**: Flask, Python
- **Database**: MongoDB
- **Client-side**: HTML, CSS, JavaScript
- **AI**: Gemini API
