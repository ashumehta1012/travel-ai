from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Load API key from environment (Render)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# PLAN PAGE
# -----------------------------
@app.route("/plan")
def plan():
    return render_template("plan.html")


# -----------------------------
# PACKAGES PAGE
# -----------------------------
@app.route("/packages")
def packages():
    return render_template("packages.html")


# -----------------------------
# AI GENERATION API
# -----------------------------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    interests = data.get("interests")

    prompt = f"""
    Create a detailed travel plan.

    Destination: {destination}
    Days: {days}
    Budget: ₹{budget}
    Interests: {interests}

    Include:
    - Day-wise itinerary
    - Places to visit
    - Food suggestions
    - Hotel recommendations
    - Estimated cost breakdown
    - Travel tips

    Keep it clean and easy to read.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart travel planner."},
                {"role": "user", "content": prompt}
            ]
        )

        plan = response.choices[0].message.content

        return jsonify({"plan": plan})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"plan": "⚠️ Error generating plan. Please try again."})


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)