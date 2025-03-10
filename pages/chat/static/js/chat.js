class ChatUI {
    constructor() {
        this.chatList = document.querySelector('.chat-list');
        this.typingInput = document.querySelector('.typing-input textarea');
        this.sendButton = document.querySelector('#send-btn');
        this.deleteButton = document.querySelector('#delete-btn');
        this.titleHeading = document.querySelector('.title-heading');
        this.secondTitleHeading = document.querySelector('.second-title-heading');
        this.loadingTemplate = document.querySelector('#loading-indicator-template');
        this.userMessageTemplate = document.querySelector('#user-message-template');
        this.chatMessageTemplate = document.querySelector('#chat-message-template');
        
        // משתנה שמציין אם הצ'אט עדיין מעבד הודעה
        this.isProcessing = false;

        this.sendButton.addEventListener('click', () => this.handleSend());
        this.deleteButton.addEventListener('click', () => this.handleDelete());

        this.typingInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // הוספת זיהוי שפה אוטומטי לתיבת הטקסט
        this.typingInput.addEventListener('input', () => this.detectLanguage());
    }

    async handleSend() {
        const message = this.typingInput.value.trim();
        if (!message || this.isProcessing) return; // אם הצ'אט עדיין מעבד הודעה, לא לשלוח הודעה חדשה
        
        // סימון שהצ'אט מעבד הודעה
        this.isProcessing = true;
        
        // שינוי מראה כפתור השליחה והשדה להראות שהם מושבתים
        this.sendButton.classList.add('disabled');
        this.deleteButton.classList.add('disabled');
        this.typingInput.classList.add('disabled');
        this.typingInput.setAttribute('placeholder', 'waiting for response...');
        this.typingInput.setAttribute('disabled', 'disabled');

        // הצגת ההודעה של המשתמש מיד
        this.addMessage(message, true);
        
        // ניקוי שדה הטקסט מיד לאחר השליחה
        this.typingInput.value = '';
        
        // השהיה קצרה לפני הצגת אינדיקטור הטעינה (0.5 שניות)
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // הוספת אינדיקטור טעינה
        const loadingIndicator = this.addLoadingIndicator();
        
        try {
            // שליחת הבקשה לשרת
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // הסרת אינדיקטור הטעינה
            this.removeLoadingIndicator(loadingIndicator);
            

            if (response.ok) {
                // הצגת התשובה מ-Gemini
                this.addMessage(data.response, false);
            } else {
                this.addMessage("Sorry, there was an error processing your request.", false);
                console.error('Error:', data.error);
            }
        } catch (error) {
            // הסרת אינדיקטור הטעינה במקרה של שגיאה
            this.removeLoadingIndicator(loadingIndicator);
        
            console.error('Error:', error);
            this.addMessage("Sorry, there was an error connecting to the server.", false);
        } finally {
            // סימון שהצ'אט סיים לעבד את ההודעה
            this.isProcessing = false;
            
            // החזרת מראה כפתור השליחה והשדה למצב רגיל
            this.sendButton.classList.remove('disabled');
            this.deleteButton.classList.remove('disabled');
            this.typingInput.classList.remove('disabled');
            this.typingInput.removeAttribute('disabled');
            this.typingInput.setAttribute('placeholder', 'Send a message');
        }
    }

    // פונקציה להוספת אינדיקטור טעינה
    addLoadingIndicator() {
        // שימוש בתבנית HTML במקום יצירת האלמנטים בקוד
        const loadingDiv = document.importNode(this.loadingTemplate.content, true).firstElementChild;
        
        this.chatList.appendChild(loadingDiv);
        this.chatList.scrollTop = this.chatList.scrollHeight;
        
        return loadingDiv;
    }
    
    // פונקציה להסרת אינדיקטור הטעינה
    removeLoadingIndicator(loadingIndicator) {
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.parentNode.removeChild(loadingIndicator);
        }
    }

    handleDelete() {
        // אם הצ'אט עדיין מעבד הודעה, לא לאפשר מחיקה
        if (this.isProcessing) return;
        
        const isConfirmed = confirm("Are you sure you want to delete your chat?");

        if (isConfirmed) {
            while (this.chatList.firstChild) {
                this.chatList.removeChild(this.chatList.firstChild);
            }

            if (this.titleHeading && this.secondTitleHeading) {
                this.titleHeading.style.display = 'block';
                this.secondTitleHeading.style.display = 'block';
            }
        }
    }

    // פונקציה חדשה לזיהוי שפה
    detectLanguage() {
        const text = this.typingInput.value;
        
        // בדיקה אם הטקסט מכיל תווים בעברית
        const hebrewPattern = /[\u0590-\u05FF]/;
        
        if (hebrewPattern.test(text)) {
            // אם יש תווים בעברית, הגדר כיוון מימין לשמאל
            this.typingInput.style.direction = 'rtl';
            this.typingInput.style.textAlign = 'right';
        } else {
            // אחרת, הגדר כיוון משמאל לימין
            this.typingInput.style.direction = 'ltr';
            this.typingInput.style.textAlign = 'left';
        }
    }

    addMessage(message, isUser) {
        if (this.titleHeading && this.secondTitleHeading) {
            this.titleHeading.style.display = 'none';
            this.secondTitleHeading.style.display = 'none';
        }

        // שימוש בתבנית המתאימה בהתאם לסוג ההודעה
        const template = isUser ? this.userMessageTemplate : this.chatMessageTemplate;
        const chatDiv = document.importNode(template.content, true).firstElementChild;
        
        const messageP = chatDiv.querySelector('p');
        
        // הגדרת כיוון הטקסט בהתאם לשפה
        const hebrewPattern = /[\u0590-\u05FF]/;
        if (hebrewPattern.test(message)) {
            messageP.style.direction = 'rtl';
            messageP.style.textAlign = 'right';
        } else {
            messageP.style.direction = 'ltr';
            messageP.style.textAlign = 'left';
        }
        
        // הוספת תוכן ההודעה
        messageP.textContent = message;
        
        this.chatList.appendChild(chatDiv);
        this.chatList.scrollTop = this.chatList.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ChatUI();
});

