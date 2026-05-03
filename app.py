from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# API Key from Render environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    interests = data.get("interests")

    prompt = f"""
    Create a detailed {days}-day travel itinerary for {destination}.
    Budget: {budget} INR
    Interests: {interests}

    Include:
    - Day-wise plan
    - Places to visit
    - Food suggestions
    - Hotel recommendations
    - Estimated cost breakdown
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({
        "result": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
