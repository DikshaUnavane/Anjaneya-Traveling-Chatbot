// chatbot/static/js/chatbot.js

const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');

// chatbot.js

// Function to send user message and receive bot response
function sendMessage(message) {
    // Placeholder for actual logic to send message to server and receive bot response
    // For demonstration purposes, we'll log the message to console and generate a placeholder response
    console.log("User Message:", message);

    // Placeholder bot response
    let botResponse = getBotResponse(message);

    // Display bot response in the chat interface
    displayMessage(botResponse, 'bot');
}

// Function to generate bot response (replace this with actual chatbot logic)
function getBotResponse(message) {
    // Placeholder logic for bot response
    // Replace this with your actual chatbot logic
    return "This is a placeholder bot response for message: " + message;
}

// Function to display messages in the chat interface
function displayMessage(message, sender) {
    // Create a new <div> element to represent the message
    let messageElement = document.createElement('div');

    // Set the CSS class based on the sender (user or bot)
    if (sender === 'user') {
        messageElement.className = 'user-message';
    } else {
        messageElement.className = 'bot-message';
    }

    // Set the text content of the message element
    messageElement.textContent = message;

    // Append the message element to the chat container
    let chatContainer = document.getElementById('chat-container');
    chatContainer.appendChild(messageElement);

    // Scroll to the bottom of the chat container to show the latest message
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listener to handle user input submission
document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Get user input from the input field
    let userInput = document.getElementById('user-input').value;

    // Display user message in the chat interface
    displayMessage(userInput, 'user');

    // Send user message to the chatbot for processing
    sendMessage(userInput);

    // Clear the input field after sending the message
    document.getElementById('user-input').value = '';
});

    

