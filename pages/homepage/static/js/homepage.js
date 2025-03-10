const homepageloginBtn = document.querySelector('.homepage-login-btn');
const homepagesignupBtn = document.querySelector('.homepage-signup-btn');
const studentBtn = document.querySelector('.role-option.student');
const lecturerBtn = document.querySelector('.role-option.lecturer');

let selectedRole = null;

studentBtn.addEventListener('click', () => {
    selectedRole = studentBtn.getAttribute('data-role');
    console.log('Selected role:', selectedRole);
    studentBtn.classList.add('selected');
    lecturerBtn.classList.remove('selected');
});

lecturerBtn.addEventListener('click', () => {
    selectedRole = lecturerBtn.getAttribute('data-role');
    console.log('Selected role:', selectedRole);
    lecturerBtn.classList.add('selected');
    studentBtn.classList.remove('selected');
});

homepagesignupBtn.addEventListener('click', (event) => {
    if (!selectedRole) {
        showErrorModal("Please select a role before proceeding.");
        shakeButtons();
        return;
    }
    
    window.location.href = `/signup/${selectedRole}`;
});

homepageloginBtn.addEventListener('click', () => {
    window.location.href = '/login';
});

function shakeButtons() {
    [studentBtn, lecturerBtn].forEach(button => {
        button.classList.remove('shake-animation');
        void button.offsetWidth;  // Trigger reflow
        button.classList.add('shake-animation');
    });
}

[studentBtn, lecturerBtn].forEach(button => {
    button.addEventListener('animationend', () => {
        button.classList.remove('shake-animation');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let selectedRole = '';
    
    document.querySelectorAll('.role-selection button').forEach(button => {
        button.addEventListener('click', function() {
            selectedRole = this.getAttribute('data-role');
        });
    });
});