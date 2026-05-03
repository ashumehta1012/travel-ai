from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI client (IMPORTANT: uses Render env variable)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")


# ✅ THIS MATCHES YOUR FRONTEND (/generate)
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    interests = data.get("interests")

    prompt = f"""
    Create a detailed travel itinerary.

    Destination: {destination}
    Days: {days}
    Budget: ₹{budget}
    Interests: {interests}

    Include:
    - Day wise plan
    - Budget breakdown
    - Food suggestions
    - Travel tips
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel planner."},
                {"role": "user", "content": prompt}
            ]
        )

        plan = response.choices[0].message.content

        return jsonify({"plan": plan})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"plan": "Error generating plan"})


if __name__ == "__main__":
    app.run(debug=True)
