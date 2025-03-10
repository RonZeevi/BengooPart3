const changePasswordBtn = document.querySelector('.change-password-btn');

document.addEventListener('DOMContentLoaded', function() {
    console.log('Profile page loaded');
    
    // Edit profile button
    const editProfileBtn = document.querySelector('.edit-profile-btn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function() {
            // Add logic for editing profile here
            alert('Profile editing functionality will be available soon');
        });
    }
    
    // Change password button
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function() {
            // ניווט לעמוד שינוי סיסמה עם הנתיב החדש
            window.location.href = '/profile/changepassword';
        });
    }
    
    // Manage access buttons
    const manageAccessBtns = document.querySelectorAll('.manage-access-btn');
    manageAccessBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const courseId = this.getAttribute('data-course-id');
            console.log(`Navigating to /courseaccess/${courseId}`);
            window.location.href = `/courseaccess/${courseId}`;
        });
    });
});