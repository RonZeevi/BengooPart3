document.addEventListener('DOMContentLoaded', function() {
    const courseSelect = document.querySelector('.course-select');
    const selectButton = document.querySelector('.btn');
    
    selectButton.addEventListener('click', function() {
        const selectedCourse = courseSelect.value;
        
        if (selectedCourse && selectedCourse !== 'בחר קורס') {
            // מעבר לדף הצ'אט עם פרמטר של הקורס הנבחר
            window.location.href = `/chat?course=${encodeURIComponent(selectedCourse)}`;
        } else {
            showErrorModal('Please select a course before proceeding');
        }
    });
});

