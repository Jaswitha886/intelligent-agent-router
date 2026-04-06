import os

html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Router</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <div class="app-layout">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Z"></path><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                    Agent Router
                </h2>
            </div>
            <div class="chat-list">
                <div class="chat-item active">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                    Current Session
                </div>
            </div>
            <div class="sidebar-footer">
                <div class="system-status">
                    <span class="pulse-dot"></span> All Systems Operational
                </div>
            </div>
        </aside>

        <!-- Main Chat -->
        <main class="chat-main">
            <header class="chat-header">
                <div class="header-title">Intelligent Agent Router</div>
            </header>

            <div id="chatContainer" class="chat-container">
                <!-- Welcome message -->
                <div class="message ai">
                    <div class="avatar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><path d="M12 12v8"></path><path d="M8 16h8"></path></svg>
                    </div>
                    <div class="msg-content welcome-card">
                        <h3>Welcome to the AI Router Server.</h3>
                        <p>Ask a complex question and I will deploy multiple agents to debate it, extracting pros, cons, and evidence to deliver a highly accurate final answer.</p>
                        <div class="suggested-prompts">
                            <button onclick="setQuery('Should our company adopt a fully remote work policy?')">Fully remote policy?</button>
                            <button onclick="setQuery('Is universal basic income a viable economic policy?')">Universal basic income?</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="input-area">
                <div class="input-wrapper">
                    <textarea id="queryInput" placeholder="Ask the AI agents anything..." rows="1" onkeydown="handleEnter(event)"></textarea>
                    <button id="sendBtn" onclick="sendMessage()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                    </button>
                </div>
                <div class="input-footer">AI agents can make mistakes. Consider verifying critical information.</div>
            </div>
        </main>
    </div>

    <script>
        marked.setOptions({ breaks: true });

        const queryInput = document.getElementById('queryInput');
        const chatContainer = document.getElementById('chatContainer');
        const sendBtn = document.getElementById('sendBtn');

        function setQuery(text) {
            queryInput.value = text;
            queryInput.focus();
            sendMessage();
        }

        function handleEnter(e) {
            if(e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        }

        queryInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
            if(this.value === '') this.style.height = 'auto';
        });

        async function sendMessage() {
            const query = queryInput.value.trim();
            if(!query) return;

            appendUserMessage(query);
            queryInput.value = '';
            queryInput.style.height = 'auto';
            
            const loadingId = appendAILoading();
            
            try {
                const res = await fetch("http://127.0.0.1:8000/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();
                
                if(!res.ok) throw new Error(data.detail || `Server returned HTTP ${res.status}`);
                renderAIResponse(loadingId, data);
            } catch(err) {
                document.getElementById(loadingId).innerHTML = `<div class="avatar"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><path d="M12 12v8"></path><path d="M8 16h8"></path></svg></div>
                    <div class="msg-content error-msg">${err.message}</div>`;
            }
        }

        function appendUserMessage(text) {
            const msgHTML = `<div class="message user"><div class="msg-content">${text}</div></div>`;
            chatContainer.insertAdjacentHTML('beforeend', msgHTML);
            scrollToBottom();
        }

        function appendAILoading() {
            const id = 'loading-' + Date.now();
            const msgHTML = `
                <div class="message ai" id="${id}">
                    <div class="avatar"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><path d="M12 12v8"></path><path d="M8 16h8"></path></svg></div>
                    <div class="msg-content"><div class="typing-indicator"><span></span><span></span><span></span></div></div>
                </div>`;
            chatContainer.insertAdjacentHTML('beforeend', msgHTML);
            scrollToBottom();
            return id;
        }

        function renderAIResponse(id, data) {
            const el = document.getElementById(id);
            let innerHTML = `<div class="avatar"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><path d="M12 12v8"></path><path d="M8 16h8"></path></svg></div><div class="msg-content ai-response-content">`;
            
            if(data.mode === 'single') {
                innerHTML += `
                    <div class="card final-card glass">
                        <h4><span class="icon">✨</span> Final Answer</h4>
                        <div class="card-body">${marked.parse(data.final || "")}</div>
                    </div>`;
            } else {
                innerHTML += `
                    <div class="debate-grid">
                        <div class="card pro-card glass">
                            <h4><span class="icon">👍</span> Pros</h4>
                            <div class="card-body">${marked.parse(data.pro || "")}</div>
                        </div>
                        <div class="card con-card glass">
                            <h4><span class="icon">👎</span> Cons</h4>
                            <div class="card-body">${marked.parse(data.con || "")}</div>
                        </div>
                    </div>
                    <div class="card evidence-card glass">
                        <h4><span class="icon">🔍</span> Supporting Evidence</h4>
                        <div class="card-body">${marked.parse(data.evidence || "")}</div>
                    </div>
                    <div class="card final-card glass highlight-glow">
                        <h4><span class="icon">⚖️</span> Final Decision</h4>
                        <div class="card-body">${marked.parse(data.final || "")}</div>
                    </div>`;
            }
            innerHTML += `</div>`;
            el.innerHTML = innerHTML;
            scrollToBottom();
        }

        function scrollToBottom() {
            setTimeout(() => {
                chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
            }, 50);
        }
    </script>
</body>
</html>"""

css = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-main: #09090b;
    --bg-panel: #18181b;
    --border-color: rgba(255, 255, 255, 0.08);
    --text-main: #e4e4e7;
    --text-muted: #a1a1aa;
    --primary: #6366f1;
    --primary-glow: rgba(99, 102, 241, 0.4);
    
    --pro-bg: rgba(34, 197, 94, 0.04);
    --con-bg: rgba(239, 68, 68, 0.04);
    --evidence-bg: rgba(255, 255, 255, 0.02);
    --final-bg: linear-gradient(145deg, rgba(139, 92, 246, 0.08), rgba(79, 70, 229, 0.08));
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', -apple-system, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    height: 100vh;
    display: flex;
    overflow: hidden;
}

.app-layout {
    display: flex;
    width: 100%;
    height: 100%;
}

/* Sidebar */
.sidebar {
    width: 260px;
    background: var(--bg-panel);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    padding: 20px;
    position: relative;
}

.sidebar-header h2 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.chat-list { flex: 1; }

.chat-item {
    padding: 12px;
    border-radius: 12px;
    font-size: 14px;
    cursor: pointer;
    color: var(--text-muted);
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}
.chat-item.active, .chat-item:hover {
    background: rgba(255,255,255,0.06);
    color: var(--text-main);
}

.sidebar-footer {
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}
.system-status {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 8px;
}
.pulse-dot {
    width: 8px; height: 8px; background: #10b981; border-radius: 50%;
    box-shadow: 0 0 8px #10b981; animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16,185,129,0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

/* Chat Main */
.chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: radial-gradient(circle at top, rgba(99,102,241,0.03), transparent 50%), var(--bg-main);
    position: relative;
}

.chat-header {
    padding: 18px 24px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    background: rgba(9, 9, 11, 0.6);
    z-index: 10;
}
.header-title { font-weight: 500; font-size: 15px; letter-spacing: 0.5px; opacity: 0.9; }

.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    gap: 32px;
}

/* Messages */
.message {
    display: flex;
    gap: 16px;
    max-width: 850px;
    margin: 0 auto;
    width: 100%;
    animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 36px; height: 36px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; background: var(--bg-panel); color: white;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.user { justify-content: flex-end; }
.user .msg-content {
    background: linear-gradient(135deg, var(--primary), #8b5cf6);
    color: white; padding: 14px 22px;
    border-radius: 20px 20px 4px 20px; font-size: 15px;
    max-width: 75%; box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
    line-height: 1.6;
}

.ai .msg-content {
    flex: 1; font-size: 15px; line-height: 1.6;
}

.welcome-card { padding-top: 6px; }
.welcome-card h3 { margin-bottom: 8px; font-size: 18px; font-weight: 600; color: white; }
.welcome-card p { color: var(--text-muted); margin-bottom: 16px; }
.suggested-prompts { display: flex; gap: 10px; flex-wrap: wrap; }
.suggested-prompts button {
    background: var(--bg-panel); border: 1px solid var(--border-color);
    padding: 8px 16px; border-radius: 20px; color: var(--text-main);
    font-size: 13px; cursor: pointer; transition: 0.2s;
}
.suggested-prompts button:hover { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3); }

/* Structured Response Cards */
.ai-response-content { display: flex; flex-direction: column; gap: 16px; }
.debate-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.card {
    background: var(--bg-panel);
    border: 1px solid var(--border-color);
    border-radius: 20px; padding: 22px;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
}
.glass { backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); background: rgba(24, 24, 27, 0.4); }
.card:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.15); }

.card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
}
.pro-card::before { background: #4ade80; }
.con-card::before { background: #f87171; }
.evidence-card::before { background: #94a3b8; }
.final-card::before { display: none; }

.pro-card { background: var(--pro-bg); }
.con-card { background: var(--con-bg); }
.evidence-card { background: var(--evidence-bg); }
.final-card {
    background: var(--final-bg);
    border: 1px solid rgba(139, 92, 246, 0.4);
    box-shadow: 0 10px 40px rgba(139, 92, 246, 0.1);
}

.card h4 {
    display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
    font-size: 15px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
.pro-card h4 { color: #4ade80; }
.con-card h4 { color: #f87171; }
.evidence-card h4 { color: #cbd5e1; }
.final-card h4 { color: #c4b5fd; }

.card-body p { margin-bottom: 12px; }
.card-body p:last-child { margin-bottom: 0; }
.card-body ul, .card-body ol { padding-left: 24px; margin-bottom: 12px; }
.card-body li { margin-bottom: 8px; }
.card-body li::marker { color: var(--text-muted); }
.card-body strong { color: white; }

/* Typing Indicator */
.typing-indicator {
    display: inline-flex; gap: 6px; padding: 14px 18px;
    background: rgba(255,255,255,0.03); border-radius: 16px;
    border: 1px solid var(--border-color); margin-top: 6px;
}
.typing-indicator span {
    width: 6px; height: 6px; background: var(--text-muted); border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

/* Input Area */
.input-area {
    padding: 24px 32px; background: linear-gradient(180deg, transparent, var(--bg-main) 30%);
    position: relative; z-index: 10;
}
.input-wrapper {
    max-width: 800px; margin: 0 auto; position: relative;
    display: flex; align-items: flex-end; background: var(--bg-panel);
    border: 1px solid var(--border-color); border-radius: 28px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5); transition: 0.3s;
}
.input-wrapper:focus-within {
    border-color: var(--primary); box-shadow: 0 0 0 2px var(--primary-glow), 0 10px 40px rgba(0,0,0,0.5);
    background: rgba(39, 39, 42, 0.8);
}

textarea {
    flex: 1; background: transparent; border: none; color: white;
    padding: 20px 24px; font-family: inherit; font-size: 15px;
    resize: none; max-height: 250px; outline: none; line-height: 1.5;
}
textarea::placeholder { color: var(--text-muted); }

.input-wrapper button {
    background: #e4e4e7; color: var(--bg-main); border: none; border-radius: 50%;
    width: 38px; height: 38px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; margin: 12px 16px 12px 8px; transition: 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.input-wrapper button:hover { transform: scale(1.1); background: white; }

.input-footer { text-align: center; font-size: 12px; color: var(--text-muted); margin-top: 14px; }
.error-msg { background: rgba(239,68,68,0.1); color: #fca5a5; border: 1px solid rgba(239,68,68,0.2); padding: 16px; border-radius: 12px; }

@media (max-width: 768px) {
    .sidebar { display: none; }
    .debate-grid { grid-template-columns: 1fr; }
    .user .msg-content { max-width: 90%; }
    .chat-container { padding: 20px 16px; }
    .input-area { padding: 16px; }
}"""

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("frontend/style.css", "w", encoding="utf-8") as f:
    f.write(css)

print("UI OVERHAUL COMPLETE")
