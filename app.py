from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Flask app object
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Chatbot logic
def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    if any(greet in user_input for greet in ["hello", "hi", "hey"]):
        return "Hello! 👋 How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "name" in user_input:
        return "I'm your friendly Flask chatbot 🤖."
    elif any(bye in user_input for bye in ["bye", "goodbye"]):
        return "Goodbye! Have a great day 😊"
    elif "time" in user_input:
        return datetime.now().strftime("The current time is %H:%M:%S ⏰")
    elif "date" in user_input:
        return datetime.now().strftime("Today's date is %Y-%m-%d 📅")
    elif any(thank in user_input for thank in ["thanks", "thank you"]):
        return "You're welcome! 😄"
    else:
        return "Sorry, I don't understand that yet."

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

# Local test
if __name__ == "__main__":
    app.run(debug=True)
