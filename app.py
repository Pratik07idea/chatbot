from flask import Flask, render_template, request, jsonify
from datetime import datetime

# ---------------------------
# Flask app object
# ---------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ---------------------------
# Chatbot logic
# ---------------------------
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # ---------------------------
    # Greetings
    # ---------------------------
    if any(greet in user_input for greet in ["hello", "hi", "hey"]):
        return "Hello! 👋 How can I help you today?"

    # How are you
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    # Bot's name
    elif "name" in user_input:
        return "I'm your friendly Flask chatbot 🤖."

    # Goodbye
    elif any(bye in user_input for bye in ["bye", "goodbye"]):
        return "Goodbye! Have a great day 😊"

    # Time
    elif "time" in user_input:
        return datetime.now().strftime("The current time is %H:%M:%S ⏰")

    # Date
    elif "date" in user_input:
        return datetime.now().strftime("Today's date is %Y-%m-%d 📅")

    # Thanks
    elif any(thank in user_input for thank in ["thanks", "thank you"]):
        return "You're welcome! 😄"

    # ---------------------------
    # Calculation problems
    # ---------------------------
    try:
        # Remove words like "calculate" or "what is"
        expr = user_input.replace("calculate", "").replace("what is", "").strip()
        expr = expr.replace("x", "*").replace("X", "*").replace("÷", "/").replace("^", "**")

        # Only allow numbers and operators
        allowed_chars = "0123456789+-*/(). "
        if all(char in allowed_chars for char in expr):
            result = eval(expr)
            return f"The answer is {result}"
    except:
        pass

    # ---------------------------
    # Basic knowledge about India
    # ---------------------------
    india_knowledge = {
        "capital": "New Delhi 🏛️",
        "largest city": "Mumbai 🏙️",
        "population": "About 1.4 billion (2025) 🇮🇳",
        "language": "Hindi 🇮🇳 (official), English widely used",
        "currency": "Indian Rupee (₹)",
        "national animal": "Bengal Tiger 🐅",
        "national bird": "Peacock 🦚",
        "national flower": "Lotus 🌸",
        "national fruit": "Mango 🥭",
        "national emblem": "Lion Capital of Ashoka 🦁"
    }

    for key, value in india_knowledge.items():
        if key in user_input:
            return f"{key.capitalize()} of India: {value}"

    # ---------------------------
    # Default fallback
    # ---------------------------
    return "Sorry, I don't understand that yet. You can ask me calculations or basic info about India."

# ---------------------------
# Routes
# ---------------------------
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

# ---------------------------
# Local test
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
