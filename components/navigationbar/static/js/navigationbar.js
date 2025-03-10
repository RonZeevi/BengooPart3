const navsignoutBtn = document.querySelector('.navsignout-btn');
const aboutUsBtn = document.querySelector('.aboutus-btn');
const navloginBtn = document.querySelector('.loginnav-btn');

if (navsignoutBtn) {
    navsignoutBtn.addEventListener('click', () => {
        window.location.href = '/signout';  
    });
}

if (navloginBtn) {
    navloginBtn.addEventListener('click', () => {
        window.location.href = '/login';  
    });
}

if (aboutUsBtn) {
    aboutUsBtn.addEventListener('click', () => {
        window.location.href = '/aboutus';  
    });
}

function goBack() {
    window.history.back();
}

function login() {
    window.location.href = '/login';
}

function signOut() {
    window.location.href = '/signout';
}

function startLearn() {
    window.location.href = '/selectcourse';
}

