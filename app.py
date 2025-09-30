"""
Flask Chatbot with extended knowledge
- Greets, small-talk, time/date
- Math calculation (safe eval)
- Basic knowledge about India
- Basic knowledge about AI
- More small-talk responses
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import ast
import operator as op

# ---------------------------
# Flask app object
# ---------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ---------------------------
# Safe math evaluation
# ---------------------------
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def safe_eval(expr: str):
    expr = expr.replace("^", "**").replace("×", "*").replace("÷", "/")
    node = ast.parse(expr, mode="eval").body

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    return _eval(node)

# ---------------------------
# Knowledge bases
# ---------------------------
INDIA_KNOWLEDGE = {
    "capital": "New Delhi 🏛️",
    "largest city": "Mumbai 🏙️",
    "population": "About 1.4 billion (2025) 🇮🇳",
    "language": "Hindi (official), English widely used",
    "currency": "Indian Rupee (₹)",
    "national animal": "Bengal Tiger 🐅",
    "national bird": "Peacock 🦚",
    "national flower": "Lotus 🌸",
    "national fruit": "Mango 🥭",
    "national emblem": "Lion Capital of Ashoka 🦁"
}

AI_KNOWLEDGE = {
    "definition": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
    "types": "Types of AI include Narrow AI (specialized), General AI (human-level), and Superintelligent AI.",
    "applications": "AI is used in healthcare, self-driving cars, virtual assistants, finance, education, and more.",
    "ml": "Machine Learning (ML) is a subset of AI where machines learn from data without being explicitly programmed.",
    "dl": "Deep Learning (DL) is a subset of ML that uses neural networks with many layers to process complex data like images and speech.",
    "nlp": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and respond to human language.",
    "robotics": "Robotics integrates AI to allow robots to perceive, plan, and act in the physical world.",
    "future": "The future of AI includes advancements in autonomous systems, creative AI, ethical AI, and human-AI collaboration."
}

# ---------------------------
# Chatbot logic
# ---------------------------
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # Greetings
    if any(greet in user_input for greet in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "Hello! 👋 How can I help you today?"

    # How are you
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    # Bot's name
    elif "name" in user_input:
        return "I'm your friendly Flask chatbot 🤖."

    # Goodbye
    elif any(bye in user_input for bye in ["bye", "goodbye", "see you"]):
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

    # Tell a joke
    elif "joke" in user_input:
        return "Why did the computer go to the doctor? Because it caught a virus! 💻🤒"

    # AI Knowledge
    for key, value in AI_KNOWLEDGE.items():
        if key in user_input:
            return f"AI {key.capitalize()}: {value}"

    if "what is ai" in user_input or "artificial intelligence" in user_input:
        return AI_KNOWLEDGE["definition"]

    # India Knowledge
    for key, value in INDIA_KNOWLEDGE.items():
        if key in user_input:
            return f"{key.capitalize()} of India: {value}"

    # Calculation problems
    try:
        expr = user_input.replace("calculate", "").replace("what is", "").strip()
        if expr:
            result = safe_eval(expr)
            return f"The answer is {result}"
    except:
        pass

    # Default fallback
    return "Sorry, I don't understand that yet. You can ask me calculations, info about India, or AI basics."

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
