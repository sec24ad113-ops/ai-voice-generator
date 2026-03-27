from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid

app = Flask(__name__)

AUDIO_FOLDER = os.path.join("static", "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    return jsonify({"success": False, "error": "Voice cloning requires upgraded plan."}), 503

@app.route("/generate-ai", methods=["POST"])
def generate_ai():
    return jsonify({"success": False, "error": "AI voice requires upgraded plan."}), 503

@app.route("/generate-rajini", methods=["POST"])
def generate_rajini():
    return jsonify({"success": False, "error": "Rajini voice requires upgraded plan."}), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
