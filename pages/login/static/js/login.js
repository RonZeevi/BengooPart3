const passwordInput = document.querySelector('input[type="password"]');
const toggleButton = document.querySelector('.passvisibility img');
const forgotPasswordLink = document.querySelector('.hyperlink');
const usernameInput = document.querySelector('input[name="username"]');
const loginBtn = document.querySelector('.btn');

// validation function
const validateUsername = (username) => {
    if (username === '') {
        return 'Username is required';
    }

    if (username.includes(' ')) {
        return 'Username cannot contain spaces';
    }

    if (username.length < 3) {
        return 'Username must be at least 3 characters long';
    }

    if (username.length > 20) {
        return 'Username cannot be longer than 20 characters';
    }

    if (!/^[a-zA-Z0-9]+$/.test(username)) {
        return 'Username can only contain English letters and numbers';
    }

    return '';
};

const validatePassword = (password) => {
    if (password === '') {
        return 'Password is required';
    }

    if (password.length < 8) {
        return 'Password must be at least 8 characters long';
    }

    if (!/[A-Z]/.test(password)) {
        return 'Password must contain at least one uppercase letter';
    }

    if (!/[0-9]/.test(password)) {
        return 'Password must contain at least one number';
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        return 'Password must contain at least one special character';
    }

    return '';
};

function showErrorModal(message) {
    const modal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const closeBtn = document.getElementsByClassName('close')[0];
    
    errorMessage.textContent = message;
    modal.style.display = 'block';
    
    // סגירת החלון בלחיצה על X
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
    
    // סגירה אוטומטית אחרי 5 שניות
    setTimeout(function() {
        modal.style.display = 'none';
    }, 5000);
}

loginBtn.addEventListener('click', (e) => {
    e.preventDefault();

    // user vailidation
    const usernameError = validateUsername(usernameInput.value);
    if (usernameError) {
        showErrorModal(usernameError);
        usernameInput.focus();
        return;
    }

    // pass vailidation
    const passwordError = validatePassword(passwordInput.value);
    if (passwordError) {
        showErrorModal(passwordError);
        passwordInput.focus();
        return;
    }

    // קבלת הטופס והנתונים
    const form = document.querySelector('form.FormDesign');
    const formData = new FormData(form);

    // fetch
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.redirected) {
            // אם השרת מבצע הפניה, עקוב אחריה
            window.location.href = response.url;
        } else {
            // אחרת, קבל את התגובה כ-JSON
            return response.json();
        }
    })
    .then(data => {
        if (data && data.error) {
            // אם יש הודעת שגיאה, הצג אותה
            showErrorModal(data.error);
            // נקה את שדה הסיסמה אבל השאר את שם המשתמש
            passwordInput.value = '';
            
            // הסר את האירוע של סגירה אוטומטית
            const modal = document.getElementById('errorModal');
            const closeBtn = document.querySelector('.close');
            
            // סגירת החלון רק בלחיצה על X
            closeBtn.onclick = function() {
                modal.style.display = 'none';
            }
            
            // סגירת החלון בלחיצה מחוץ למודל
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }
        } else if (data && data.success) {
            // אם ההתחברות הצליחה, עבור לדף הבא
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorModal('An error occurred during login. Please try again later.');
    });
});

toggleButton.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.src = 'static/media/img/view.png';
    } else {
        passwordInput.type = 'password';
        toggleButton.src = 'static/media/img/hide.png';
    }
});


if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener('click', (e) => {
        e.preventDefault();


        if (!usernameInput.value.trim()) {
            showErrorModal("Please enter your username first to receive password reset instructions.");
            usernameInput.focus();
            return;
        }
        
        // בדיקת תקינות שם המשתמש
        const usernameError = validateUsername(usernameInput.value);
        if (usernameError) {
            showErrorModal(usernameError);
            usernameInput.focus();
            return;
        }

        // שליחת בקשה לשרת לבדיקת קיום המשתמש ולקבלת המייל שלו
        fetch('/check-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ username: usernameInput.value })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                // אם המשתמש קיים, הצג הודעה עם המייל האמיתי שלו
                showErrorModal(`Password reset instructions have been sent to ${data.email}`);
                
                // שליחת בקשה לשרת לשליחת מייל איפוס סיסמה
                fetch('/reset-password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ username: usernameInput.value })
                });
            } else {
                // אם המשתמש לא קיים, הצג הודעת שגיאה
                showErrorModal("The username you entered does not exist in the system.");
                usernameInput.focus();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorModal("An error occurred while checking the username. Please try again later.");
        });
    });
}



