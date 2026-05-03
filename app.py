from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Load API key from environment
client = OpenAI(api_key=os.getenv("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"))

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# AI ITINERARY GENERATION
# -----------------------------
def generate_itinerary(destination, days, budget, interests):
    prompt = f"""
    Create a detailed {days}-day travel itinerary for {destination}.

    Budget: {budget}
    Interests: {interests}

    Include:
    - Day-wise plan
    - Places to visit
    - Food suggestions
    - Estimated budget breakdown
    - Travel tips

    Make it clean and easy to read.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# API ROUTE (Frontend calls this)
# -----------------------------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    interests = data.get("interests")

    result = generate_itinerary(destination, days, budget, interests)

    return jsonify({"result": result})


# -----------------------------
# TEST ROUTE (optional)
# -----------------------------
@app.route("/test")
def test():
    return generate_itinerary("Manali", 2, "10000", "adventure, mountains")


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
