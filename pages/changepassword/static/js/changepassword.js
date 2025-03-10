document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('changePasswordForm');
    const currentPasswordInput = document.querySelector('input[name="current_password"]');
    const newPasswordInput = document.querySelector('input[name="new_password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const toggleButtons = document.querySelectorAll('.passvisibility');
    
    // אלמנטים של דרישות הסיסמה
    const lengthRequirement = document.getElementById('length-requirement');
    const uppercaseRequirement = document.getElementById('uppercase-requirement');
    const numberRequirement = document.getElementById('number-requirement');
    const specialRequirement = document.getElementById('special-requirement');
    
    // פונקציה לבדיקת תקינות הסיסמה ועדכון האייקונים
    function validatePassword(password) {
        // איפוס כל האייקונים
        lengthRequirement.classList.remove('valid');
        uppercaseRequirement.classList.remove('valid');
        numberRequirement.classList.remove('valid');
        specialRequirement.classList.remove('valid');
        
        if (password === '') {
            return 'Password is required';
        }

        // בדיקת אורך
        if (password.length >= 8) {
            lengthRequirement.classList.add('valid');
        }

        // בדיקת אות גדולה
        if (/[A-Z]/.test(password)) {
            uppercaseRequirement.classList.add('valid');
        }

        // בדיקת מספר
        if (/[0-9]/.test(password)) {
            numberRequirement.classList.add('valid');
        }

        // בדיקת תו מיוחד
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            specialRequirement.classList.add('valid');
        }
        
        // בדיקה אם כל הדרישות מתקיימות
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
    }
    
    // הוספת אירוע לשדה הסיסמה החדשה לבדיקת הדרישות בזמן אמת
    newPasswordInput.addEventListener('input', function() {
        validatePassword(this.value);
    });
    
    // הוספת אירוע לחיצה לכפתורי הצגת/הסתרת סיסמה
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.parentElement.querySelector('input');
            const img = this.querySelector('img');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                img.src = '/static/media/img/view.png';
            } else {
                passwordInput.type = 'password';
                img.src = '/static/media/img/hide.png';
            }
        });
    });
    
    // הוספת אירוע שליחת טופס
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // בדיקת תקינות הסיסמה הנוכחית
        if (!currentPasswordInput.value) {
            showErrorModal('Please enter your current password');
            currentPasswordInput.focus();
            return;
        }
        
        // בדיקת תקינות הסיסמה החדשה
        const passwordError = validatePassword(newPasswordInput.value);
        if (passwordError) {
            showErrorModal(passwordError);
            newPasswordInput.focus();
            return;
        }
        
        // בדיקה שהסיסמאות תואמות
        if (newPasswordInput.value !== confirmPasswordInput.value) {
            showErrorModal('Passwords do not match');
            confirmPasswordInput.focus();
            return;
        }
        
        // בדיקה שהסיסמה החדשה שונה מהסיסמה הנוכחית
        if (newPasswordInput.value === currentPasswordInput.value) {
            showErrorModal('New password must be different from current password');
            newPasswordInput.focus();
            return;
        }
        
        // שליחת הנתונים לשרת
        fetch('/profile/api/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                current_password: currentPasswordInput.value,
                new_password: newPasswordInput.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // אם השינוי הצליח, הצג הודעת הצלחה והפנה לדף הפרופיל
                alert('Password changed successfully!');
                window.location.href = '/profile';
            } else {
                // אם יש שגיאה, הצג אותה
                showErrorModal(data.error || 'Failed to change password');
                
                // אם השגיאה קשורה לסיסמה הנוכחית, נקה את השדה ושים פוקוס עליו
                if (data.error && data.error.includes('current password')) {
                    currentPasswordInput.value = '';
                    currentPasswordInput.focus();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorModal('An error occurred. Please try again later.');
        });
    });
});
