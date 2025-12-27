document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const resetBtn = document.getElementById('reset-btn');

    // Generate or retrieve Session/User IDs
    let userId = localStorage.getItem('rc_user_id');
    if (!userId) {
        userId = crypto.randomUUID();
        localStorage.setItem('rc_user_id', userId);
    }
    
    let sessionId = sessionStorage.getItem('rc_session_id');
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        sessionStorage.setItem('rc_session_id', sessionId);
    }

    // Scroll to bottom
    const scrollToBottom = () => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // Add Message to UI
    const addMessage = (content, isUser, isHtml = false) => {
        const wrapper = document.createElement('div');
        wrapper.className = `flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`;
        
        const avatar = document.createElement('div');
        avatar.className = `w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs ${isUser ? 'bg-slate-400' : 'bg-teal-600'}`;
        avatar.textContent = isUser ? 'You' : 'AI';

        const bubble = document.createElement('div');
        bubble.className = `${isUser ? 'bg-teal-600 text-white' : 'bg-white border border-slate-100 text-slate-700'} p-4 rounded-2xl shadow-sm max-w-[85%] ${isUser ? 'rounded-tr-none' : 'rounded-tl-none'} markdown-body`;
        
        if (isHtml) {
            bubble.innerHTML = content;
        } else {
            bubble.textContent = content;
        }

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        messagesContainer.appendChild(wrapper);
        scrollToBottom();
    };

    // Handle Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        // UI Updates
        addMessage(text, true);
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;
        
        // Loader
        const loadingId = 'loading-' + Date.now();
        const loaderWrapper = document.createElement('div');
        loaderWrapper.id = loadingId;
        loaderWrapper.className = 'flex gap-4';
        loaderWrapper.innerHTML = `
            <div class="w-8 h-8 bg-teal-600 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs">AI</div>
            <div class="bg-white border border-slate-100 p-4 rounded-2xl rounded-tl-none shadow-sm flex gap-1 items-center">
                <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
        `;
        messagesContainer.appendChild(loaderWrapper);
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    user_id: userId,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            // Remove loader
            document.getElementById(loadingId).remove();

            if (data.error) {
                addMessage("I'm having trouble connecting right now.", false);
            } else {
                addMessage(data.response, false, true); // Render HTML
            }

        } catch (error) {
            document.getElementById(loadingId).remove();
            addMessage("Network connection error. Please try again.", false);
            console.error(error);
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    });

    // Reset
    resetBtn.addEventListener('click', () => {
        if(confirm("Start a new conversation? This will clear the current chat view.")) {
            sessionStorage.removeItem('rc_session_id'); // New session
            location.reload();
        }
    });
});
