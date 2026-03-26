from flask import Flask, render_template, request, jsonify, url_for
from TTS.api import TTS
import os
import uuid
import torch

app = Flask(__name__)

# 📁 Folders
AUDIO_FOLDER = os.path.join("static", "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# 🎧 Your original voice file (for playback + cloning)
MY_VOICE = os.path.join("static", "hanirecording.wav")

# ⚡ Device
device = "cuda" if torch.cuda.is_available() else "cpu"

# 🤖 Load AI model
tts = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        global tts
        if tts is None:
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
                
        text = request.form.get("text", "").strip()
        language = request.form.get("language", "en")

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        if not os.path.exists(MY_VOICE):
            return jsonify({
                "success": False,
                "error": "Voice file not found in static folder"
            }), 500

        # 🎤 Generated audio file
        filename = f"speech_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_FOLDER, filename)

        # 🔊 Generate AI voice using your recording
        tts.tts_to_file(
            text=text,
            speaker_wav=MY_VOICE,
            language=language,
            file_path=output_path
        )

        return jsonify({
            "success": True,
            "audio_url": url_for('static', filename=f"audio/{filename}")
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)