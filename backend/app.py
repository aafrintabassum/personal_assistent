from flask import Flask, request, jsonify
from flask_cors import CORS

# create flask app
app = Flask(__name__)

# allow frontend to connect
CORS(app)

# home route (optional)
@app.route("/")
def home():
    return "Backend is running"

# chat route (MAIN PART)
@app.route("/chat", methods=["POST"])
def chat():

    # get message from frontend
    data = request.json
    user_message = data.get("message")

    print("User message:", user_message)

    # bot logic (simple reply for now)
    bot_reply = "You said: " + user_message

    # send reply back
    return jsonify({
        "reply": bot_reply
    })


# run server
if __name__ == "__main__":
    app.run(debug=True)
