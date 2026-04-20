document.addEventListener("DOMContentLoaded", () => {
    // UI Elements
    const chatbotToggle = document.getElementById("chatbot-toggle");
    const chatWindow = document.getElementById("chat-window");
    const closeChatBtn = document.getElementById("close-chat");
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const sendMessageBtn = document.getElementById("send-message");

    // State tracking
    let hasGreeted = false;

    // Helper: Add a message bubble to the chat
    const appendMessage = (text, sender) => {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", `${sender}-message`);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Helper: Show/Hide typing indicator
    const showTypingIndicator = () => {
        const typingDiv = document.createElement("div");
        typingDiv.classList.add("typing-indicator");
        typingDiv.id = "typing-bot";
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const hideTypingIndicator = () => {
        const indicator = document.getElementById("typing-bot");
        if (indicator) {
            indicator.remove();
        }
    };

    // Toggle Chat Window logic
    const toggleChat = () => {
        chatWindow.classList.toggle("hidden");
        
        // If opening the chat for the first time, greet the user
        if (!chatWindow.classList.contains("hidden")) {
            chatInput.focus();
            if (!hasGreeted) {
                hasGreeted = true;
                showTypingIndicator();
                setTimeout(() => {
                    hideTypingIndicator();
                    appendMessage("Hi there! 👋 I'm your database assistant. What would you like to know today?", "bot");
                }, 800); // Small delay to make it feel natural
            }
        }
    };

    // Event Listeners for opening and closing
    chatbotToggle.addEventListener("click", toggleChat);
    closeChatBtn.addEventListener("click", () => chatWindow.classList.add("hidden"));

    // Handle sending message to backend
    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text) return; // Don't send empty messages

        // 1. Display user message
        appendMessage(text, "user");
        chatInput.value = ""; // Clear input immediately
        
        // 2. Show bot "typing" animation
        showTypingIndicator();

        try {
            // 3. Make POST request to our FastAPI backend
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text }) // Send user text
            });

            // 4. Handle response
            const data = await response.json();
            hideTypingIndicator();

            if (response.ok) {
                appendMessage(data.reply, "bot");
            } else {
                // If the backend returned a 400/500 error
                appendMessage("Oops! Something went wrong: " + (data.detail || "Unknown error"), "bot");
            }
        } catch (error) {
            // If the server is unreachable
            hideTypingIndicator();
            appendMessage("Error: Could not connect to the server. Make sure it is running.", "bot");
            console.error("Chat error:", error);
        }
    };

    // Send when clicking the send icon
    sendMessageBtn.addEventListener("click", sendMessage);

    // Send when pressing 'Enter' inside the input field
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
