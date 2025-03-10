// פונקציה גלובלית להצגת חלון קופץ מינימליסטי עם הודעת שגיאה
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
    
    // סגירת החלון בלחיצה מחוץ למודל
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
    
    // סגירה אוטומטית אחרי 5 שניות (אופציונלי)
    setTimeout(function() {
        if (modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    }, 5000);
}

// בדיקה אם יש אלמנט שמכיל נתוני שגיאה בטעינת הדף
document.addEventListener('DOMContentLoaded', function() {
    const errorDataElement = document.getElementById('error-data');
    if (errorDataElement && errorDataElement.dataset.error) {
        showErrorModal(errorDataElement.dataset.error);
    }
});
