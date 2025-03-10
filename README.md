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

| Role | Username | Password |
|------|----------|----------|
| Student | ronzeev | 123123Ab! |
| Lecturer | arseniy | 123123Ab!! |

These example accounts can be used to test the system without creating new users.

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
<img width="960" alt="image" src="https://github.com/user-attachments/assets/18c81db9-11c2-4f63-be9f-7ad9d0e32f13" />

Registration page with fields for personal information and role selection.

### Login Page
<img width="958" alt="image" src="https://github.com/user-attachments/assets/d7a5ff20-bcc2-40c4-9333-7c4b38cde1f7" />

Login page for registered users.

### User Profile
<img width="941" alt="image" src="https://github.com/user-attachments/assets/74a53b6a-ff9b-43c3-a220-0f4efac24c94" />

The profile page displays user details and their course list.

### Course Selection
<img width="954" alt="image" src="https://github.com/user-attachments/assets/9d8ff55d-2158-4119-8345-3f27e63ceece" />

Page for selecting a course from the list of courses available to the user.

### Course Access Management
<img width="940" alt="image" src="https://github.com/user-attachments/assets/d09cd58b-5193-475b-a171-d9c5f8d7c84d" />

Page that allows lecturers to manage course access (add/remove students).

### AI Chat
<img width="939" alt="image" src="https://github.com/user-attachments/assets/5a6b6773-a493-4a3b-b781-9b68ece2f41c" />

Smart chat interface based on Gemini API for course-related questions and answers.

### Change Password
<img width="952" alt="image" src="https://github.com/user-attachments/assets/e4765ccc-89f2-4051-ab8c-f251e417a66c" />

Page for changing the user's password.

### About
<img width="953" alt="image" src="https://github.com/user-attachments/assets/4e814ac1-da72-4eb9-b6f8-b9ef4b8ad5a4" />

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
