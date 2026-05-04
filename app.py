import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        destination = data.get("destination")
        days = data.get("days")
        budget = data.get("budget")
        interests = data.get("interests")

        prompt = f"""
        Create a detailed travel plan:

        Destination: {destination}
        Days: {days}
        Budget: {budget}
        Interests: {interests}

        Include:
        - Day-wise itinerary
        - Budget tips
        - Places to visit
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"result": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
