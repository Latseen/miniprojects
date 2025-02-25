from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Serves the frontend

#@app.route("/api/message")
#def api_message():
#    return jsonify({"message": "Hello from Flask API!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
