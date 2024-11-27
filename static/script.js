const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const fileUpload = document.getElementById('file-upload');

sendButton.addEventListener('click', sendMessage);
fileUpload.addEventListener('change', uploadImage);

function sendMessage() {
    const message = userInput.value.trim();
    if (message !== '') {
        appendMessage('user', message);
        userInput.value = '';

        setTimeout(() => {
            fetchAnswer(message);
        }, 500);
    }
}

function uploadImage() {
    const file = fileUpload.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        appendMessage('user', `<img src="${URL.createObjectURL(file)}" class="chat-image">`);

        fetch('/upload_image', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const recognizedObjects = data.recognized_objects.join(', ');
            appendMessage('bot', `I recognize: ${recognizedObjects}`);
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            appendMessage('bot', 'Error recognizing image. Please try again.');
        });
    }
}

function fetchAnswer(message) {
    fetch('/ask_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage('bot', data.answer);
    })
    .catch(error => {
        console.error('Error asking question:', error);
        appendMessage('bot', 'Error processing your question. Please try again.');
    });
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    messageElement.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
