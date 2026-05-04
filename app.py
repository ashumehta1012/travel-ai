import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")

        prompt = f"""
        You are an AI Travel Expert.

        Help the user with travel planning.

        Provide:
        - Best destinations (if not specified)
        - How to reach (flight/train/road)
        - Budget breakdown
        - Famous places to visit
        - Local food
        - Best time to visit
        - Tips

        User query:
        {user_input}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
