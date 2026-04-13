// Global variables
let mode = 'text';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Animate on load
    const bubble = document.getElementById('speechBubble');
    setTimeout(() => {
        bubble.classList.add('speaking');
        setTimeout(() => bubble.classList.remove('speaking'), 2000);
    }, 500);
    
    initParticles();
    console.log('Bruno ready!');
    
    // Welcome message
    setTimeout(() => {
        displayResponse("Hey beautiful! I am Bruno. How can I help you?");
    }, 1000);
});

// Particle background
const canvas = document.getElementById('background');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

function initParticles() {
    particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 1,
            vy: (Math.random() - 0.5) * 1,
            size: Math.random() * 2 + 0.5,
            alpha: Math.random() * 0.5 + 0.2
        });
    }
    animateParticles();
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        
        // Wrap around screen
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        
        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 212, 255, ${p.alpha})`;
        ctx.fill();
    });
    
    // Draw connections
    particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
            const dx = p1.x - p2.x;
            const dy = p1.y - p2.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < 150) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = `rgba(0, 212, 255, ${0.15 * (1 - dist / 150)})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        });
    });
    
    requestAnimationFrame(animateParticles);
}

// Mode toggle
document.getElementById('modeToggle').addEventListener('click', function() {
    mode = mode === 'text' ? 'voice' : 'text';
    this.textContent = mode === 'text' ? '📝 Text' : '🎤 Voice';
    document.getElementById('textInput').style.display = mode === 'text' ? 'block' : 'none';
    updateStatus(mode === 'text' ? 'Text mode' : 'Voice mode - Click mic to speak');
    console.log('Mode:', mode);
});

// Send button
document.getElementById('sendBtn').addEventListener('click', function() {
    const input = document.getElementById('textInput');
    const message = input.value.trim();
    
    if (message) {
        sendMessage(message);
        input.value = '';
    } else {
        updateStatus('Please type a message!');
    }
});

// Enter key to send
document.getElementById('textInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const message = this.value.trim();
        if (message) {
            sendMessage(message);
            this.value = '';
        }
    }
});

// Voice button
document.getElementById('voiceBtn').addEventListener('click', function() {
    if (mode === 'voice') {
        startVoiceRecognition();
    } else {
        updateStatus('Switch to Voice mode first!');
    }
});

// Browser Speech Recognition
function startVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        updateStatus('Voice recognition not supported!');
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
        updateStatus('🎤 Listening... Speak now!');
        document.getElementById('voiceBtn').classList.add('listening');
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        console.log('Voice input:', transcript);
        updateStatus('You said: ' + transcript);
        sendMessage(transcript);
    };
    
    recognition.onerror = function(event) {
        updateStatus('Error: ' + event.error);
        document.getElementById('voiceBtn').classList.remove('listening');
    };
    
    recognition.onend = function() {
        document.getElementById('voiceBtn').classList.remove('listening');
    };
    
    recognition.start();
}

// Send message to backend
function sendMessage(message) {
    if (!message) return;
    
    updateStatus('Thinking...');
    console.log('Sending:', { mode: mode, message: message });
    
    fetch('/chat', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            mode: mode, 
            message: message 
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        displayResponse(data.response);
        updateStatus('Ready');
    })
    .catch(err => {
        console.error('Error:', err);
        displayResponse('Error connecting to server!');
        updateStatus('Error');
    });
}

// Display response
function displayResponse(text) {
    const bubble = document.getElementById('speechBubble');
    document.getElementById('responseText').textContent = text;
    
    // Add animation
    bubble.classList.add('speaking');
    
    // Remove after animation
    setTimeout(() => {
        bubble.classList.remove('speaking');
    }, 3000);
}

// Update status
function updateStatus(text) {
    document.getElementById('status').textContent = text;
}

// Handle window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});