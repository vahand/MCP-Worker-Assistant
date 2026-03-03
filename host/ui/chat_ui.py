"""
Minimalist Chat UI for MCP Host using a web-based interface.
Uses Python's built-in http.server - no external dependencies required.
"""
import asyncio
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Any
import socket


# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Planning Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #1e1e1e;
            color: #e0e0e0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            padding: 16px 20px;
            background-color: #252525;
            border-bottom: 1px solid #333;
        }
        
        .header h1 {
            font-size: 18px;
            font-weight: 600;
            color: #4a9eff;
        }
        
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .message.user {
            align-self: flex-end;
            background-color: #4a9eff;
            color: white;
        }
        
        .message.assistant {
            align-self: flex-start;
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        .message.system {
            align-self: center;
            background-color: transparent;
            color: #888;
            font-size: 14px;
            font-style: italic;
        }
        
        .message.error {
            align-self: center;
            background-color: #ff4a4a20;
            color: #ff6b6b;
            border: 1px solid #ff4a4a40;
        }
        
        .input-container {
            padding: 16px 20px;
            background-color: #252525;
            border-top: 1px solid #333;
            display: flex;
            gap: 12px;
        }
        
        #message-input {
            flex: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 8px;
            background-color: #2d2d2d;
            color: #e0e0e0;
            font-size: 15px;
            outline: none;
        }
        
        #message-input:focus {
            box-shadow: 0 0 0 2px #4a9eff40;
        }
        
        #message-input::placeholder {
            color: #666;
        }
        
        #send-button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            background-color: #4a9eff;
            color: white;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        #send-button:hover:not(:disabled) {
            background-color: #3a8eef;
        }
        
        #send-button:disabled {
            background-color: #4a9eff60;
            cursor: not-allowed;
        }
        
        .status-bar {
            padding: 8px 20px;
            background-color: #1a1a1a;
            font-size: 12px;
            color: #666;
        }
        
        .typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 12px 16px;
            background-color: #2d2d2d;
            border-radius: 12px;
        }
        
        .typing-indicator.visible {
            display: flex;
            gap: 4px;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background-color: #666;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-4px); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Daily Planning Assistant</h1>
    </div>
    
    <div class="chat-container" id="chat-container">
        <div class="message system">Welcome! I can help you with your calendar and tasks.</div>
    </div>
    
    <div class="typing-indicator" id="typing-indicator">
        <span></span><span></span><span></span>
    </div>
    
    <div class="input-container">
        <input type="text" id="message-input" placeholder="Type your message..." autocomplete="off">
        <button id="send-button">Send</button>
    </div>
    
    <div class="status-bar" id="status-bar">Ready</div>
    
    <script>
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const statusBar = document.getElementById('status-bar');
        const typingIndicator = document.getElementById('typing-indicator');
        
        function addMessage(content, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function setLoading(loading) {
            sendButton.disabled = loading;
            messageInput.disabled = loading;
            typingIndicator.classList.toggle('visible', loading);
            statusBar.textContent = loading ? 'Thinking...' : 'Ready';
            if (!loading) {
                messageInput.focus();
            }
        }
        
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            messageInput.value = '';
            addMessage(message, 'user');
            setLoading(true);
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('Error: ' + data.error, 'error');
                } else {
                    addMessage(data.response, 'assistant');
                }
            } catch (error) {
                addMessage('Connection error: ' + error.message, 'error');
            } finally {
                setLoading(false);
            }
        }
        
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        messageInput.focus();
    </script>
</body>
</html>
"""


class ChatRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the chat UI."""
    
    message_callback = None
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Serve the main HTML page."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle chat messages."""
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                message = data.get('message', '')
                
                callback = ChatRequestHandler.message_callback
                if callback:
                    # Run async callback
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(callback(message))
                    loop.close()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'response': response}).encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'No callback configured'}).encode())
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()


class ChatUI:
    """A minimalist web-based chat interface for the AI assistant."""

    def __init__(self, on_message_callback: Callable[[str], Any], port: int = 8765):
        """
        Initialize the chat UI.

        Args:
            on_message_callback: Async function called when user sends a message.
            port: Port to run the web server on.
        """
        self.on_message_callback = on_message_callback
        self.port = port
        self.server = None
        
    def _find_free_port(self, start_port: int) -> int:
        """Find a free port starting from start_port."""
        port = start_port
        while port < start_port + 100:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                port += 1
        return start_port

    def run(self):
        """Start the web server and open the browser."""
        # Find available port
        self.port = self._find_free_port(self.port)
        
        # Configure the request handler
        ChatRequestHandler.message_callback = self.on_message_callback
        
        # Create and start server
        self.server = HTTPServer(('localhost', self.port), ChatRequestHandler)
        
        url = f'http://localhost:{self.port}'
        print(f"\n{'='*50}")
        print(f"  Chat UI running at: {url}")
        print(f"  Press Ctrl+C to stop")
        print(f"{'='*50}\n")
        
        # Open browser
        webbrowser.open(url)
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.server.shutdown()


def create_chat_ui(on_message_callback: Callable[[str], Any], port: int = 8765) -> ChatUI:
    """
    Create and return a ChatUI instance.

    Args:
        on_message_callback: Async function to handle user messages.
        port: Port for the web server (default: 8765).

    Returns:
        ChatUI instance ready to run.
    """
    return ChatUI(on_message_callback, port)
