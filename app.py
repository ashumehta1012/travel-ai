from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_input = data.get("preferences", "").lower()

    places = []

    if "mountains" in user_input:
        places.append({
            "name": "Manali",
            "price": "₹8,000",
            "rating": "4.6",
            "image": "https://source.unsplash.com/400x300/?manali"
        })

    if "beach" in user_input:
        places.append({
            "name": "Goa",
            "price": "₹10,000",
            "rating": "4.5",
            "image": "https://source.unsplash.com/400x300/?goa"
        })

    if "adventure" in user_input:
        places.append({
            "name": "Rishikesh",
            "price": "₹6,000",
            "rating": "4.7",
            "image": "https://source.unsplash.com/400x300/?rishikesh"
        })

    if "relaxation" in user_input:
        places.append({
            "name": "Kerala",
            "price": "₹12,000",
            "rating": "4.8",
            "image": "https://source.unsplash.com/400x300/?kerala"
        })

    return jsonify({"places": places})


if __name__ == "__main__":
    app.run(debug=True)