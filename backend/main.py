from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice import speak, listen
from brain import get_ai_response
from weather import get_weather
from news import get_news
from tasks import open_app
from memory import remember, recall, get_memory

app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    mode = request.json.get("mode", "text")
    user_message = request.json.get("message", "")
    
    print(f"Mode: {mode}, Message: {user_message}")
    
    # Voice mode - listen first
    if mode == "voice" and not user_message:
        user_message = listen()
        print(f"Listened: {user_message}")
        
        if not user_message or "sorry" in user_message.lower():
            reply = "I didn't catch that. Please speak again."
            speak(reply)
            return jsonify({"response": reply})
    
    if not user_message:
        return jsonify({"response": "Please say or type a message."})
    
    # Process message
    message = user_message.lower()
    reply = ""
    
    # === MEMORY ===
    if "remember" in message and "is" in message:
        try:
            parts = message.replace("remember", "").strip()
            if "my" in parts:
                parts = parts.replace("my", "").strip()
            
            if "is" in parts:
                key_value = parts.split("is")
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    reply = remember(key, value)
                else:
                    reply = "Say: remember my name is John"
        except:
            reply = "Say: remember my name is John"
    
    elif any(x in message for x in ["what is my", "what's my", "recall", "do you remember"]):
        if "name" in message:
            reply = recall("name")
        elif "birthday" in message:
            reply = recall("birthday")
        else:
            reply = get_memory()
    
    # === WEATHER ===
    elif "weather" in message:
        words = message.replace("what's the weather in", "").replace("what is the weather in", "")
        words = words.replace("weather in", "").replace("weather", "").strip()
        city = words if words else None
        reply = get_weather(city)
    
    # === NEWS ===
    elif "news" in message:
        reply = get_news()
    
    # === OPEN APP ===
    elif "open" in message:
        app_name = message.replace("open", "").strip()
        reply = open_app(app_name)
    
    # === GREETINGS ===
    elif any(x in message for x in ["hello", "hi", "hey", "नमस्ते"]):
        reply = "Hello Aafu! I'm Bruno. How can I help you?"
    
    # === WHO ARE YOU ===
    elif any(x in message for x in ["your name", "who are you"]):
        reply = "My name is Bruno! I'm your AI ."
    
    # === DEFAULT - USE AI ===
    else:
        reply = get_ai_response(user_message)
    
    # ALWAYS SPEAK - both text and voice mode
    print(f"Speaking: {reply}")
    speak(reply)
    
    return jsonify({"response": reply})

@app.route("/listen", methods=["GET"])
def listen_voice():
    text = listen()
    return jsonify({"text": text})

@app.route("/speak", methods=["POST"])
def speak_text():
    text = request.json.get("text", "")
    speak(text)
    return jsonify({"success": True})

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Bruno ...")
    print("Go to: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000, use_reloader=False)