// static/chatbot_app/js/chatbot.js

// Function to get CSRF token from cookies
    
    function sendMessage() {
        var userInput = document.getElementById('user-input').value;
        document.getElementById('user-input').value = '';
        var chatContainer = document.getElementById('chat-container');
        
        // Append user message to chat container
        chatContainer.innerHTML += '<p>User: ' + userInput + '</p>';
        
        // Send user input to server
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ user_input: userInput }),
        })
        .then(response => response.json())
        .then(data => {
            // Append bot response to chat container
            chatContainer.innerHTML += '<p>Bot: ' + data.response + '</p>';
        });
    }
    
    // Get CSRF token for POST requests
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
//     const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
//     return cookieValue;
// }

// // Event listener for send button click
// sendBtn.addEventListener('click', () => {
//     const userMessage = userInput.value.trim();
//     if (userMessage !== '') {
//         appendMessage('You: ' + userMessage);
//         userInput.value = ''; // Clear input field
//         // Send userMessage to backend and receive bot response
//         fetch('/chatbot/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken() // Include CSRF token in headers
//             },
//             body: JSON.stringify({'user_input': userMessage})
//         })
//         .then(response => response.json())
//         .then(data => {
//             appendMessage('Bot: ' + data.bot_response);
//         })
//         .catch(error => console.error('Error:', error));
//     }
// });
