document.addEventListener('DOMContentLoaded', function() {
    const courseId = document.getElementById('course-id').value;
    const addUserBtn = document.getElementById('add-user-btn');
    const usernameInput = document.getElementById('username-input');
    const addUserMessage = document.getElementById('add-user-message');
    const backBtn = document.querySelector('.btn'); // כפתור חזרה לפרופיל
    const usersContainer = document.querySelector('.users-section');
    const courseTitleElement = document.querySelector('.course-name');

    async function loadCourseData() {
        try {
            const response = await fetch(`/courseaccess/api/course/id/${courseId}`);
            
            if (!response.ok) {
                throw new Error('Failed to load course data');
            }
            
            const data = await response.json();
            
            // עדכון כותרת הקורס
            if (courseTitleElement) {
                courseTitleElement.textContent = data.course.course_name;
            }
            
            // עדכון רשימת המשתמשים
            renderUsersList(data.course_users);
            
        } catch (error) {
            console.error('Error loading course data:', error);
            usersContainer.innerHTML = `<p class="error">Error loading course data: ${error.message}</p>`;
        }
    }
    
    // הצגת רשימת המשתמשים
    function renderUsersList(users) {
        if (!users || users.length === 0) {
            usersContainer.innerHTML = `
                <h3>Users with Access</h3>
                <p class="no-users">No users have access to this course yet</p>
            `;
            return;
        }
        
        const usersHTML = `
            <h3>Users with Access</h3>
            <div class="users-list">
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${users.map(user => `
                            <tr>
                                <td>${user.username}</td>
                                <td>${user.fullname}</td>
                                <td>${user.email}</td>
                                <td>
                                    <button class="remove-user-btn" data-username="${user.username}">Remove</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        usersContainer.innerHTML = usersHTML;
        
        // הוספת מאזיני אירועים לכפתורי ההסרה החדשים
        document.querySelectorAll('.remove-user-btn').forEach(btn => {
            btn.addEventListener('click', handleRemoveUser);
        });
    }
    
    // טיפול בהסרת משתמש
    async function handleRemoveUser() {
        const username = this.getAttribute('data-username');
        if (confirm(`Are you sure you want to remove ${username} from this course?`)) {
            try {
                const response = await fetch('/courseaccess/api/remove', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        course_id: courseId,
                        username: username
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // רענון רשימת המשתמשים
                    loadCourseData();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        }
    }
    
    // טיפול בהוספת משתמש
    async function handleAddUser() {
        const username = usernameInput.value.trim();
        if (!username) {
            addUserMessage.textContent = 'Please enter a username';
            addUserMessage.className = 'message error';
            return;
        }
        
        try {
            const response = await fetch('/courseaccess/api/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    course_id: courseId,
                    username: username
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                addUserMessage.textContent = data.message;
                addUserMessage.className = 'message success';
                usernameInput.value = '';
                
                // רענון רשימת המשתמשים
                loadCourseData();
            } else {
                addUserMessage.textContent = data.message;
                addUserMessage.className = 'message error';
            }
        } catch (error) {
            console.error('Error:', error);
            addUserMessage.textContent = 'An error occurred. Please try again.';
            addUserMessage.className = 'message error';
        }
    }
    
    // הוספת מאזיני אירועים
    addUserBtn.addEventListener('click', handleAddUser);
    
    // חזרה לדף הפרופיל
    backBtn.addEventListener('click', function() {
        window.location.href = '/profile';
    });
    
    // טעינת נתוני הקורס בעת טעינת הדף
    loadCourseData();
});
