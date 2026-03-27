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

# 🤖 Models (loaded lazily)
tts_ai = None      # standard AI voice model (lightweight)


@app.route("/")
def index():
    return render_template("index.html")


# ── Route 1: Speak in standard AI voice ──────────────────────────────────────
@app.route("/generate-ai", methods=["POST"])
def generate_ai():
    try:
        global tts_ai
        if tts_ai is None:
            tts_ai = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)

        text = request.form.get("text", "").strip()

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        filename = f"ai_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_FOLDER, filename)

        tts_ai.tts_to_file(text=text, file_path=output_path)

        return jsonify({
            "success": True,
            "audio_url": url_for('static', filename=f"audio/{filename}")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── Route 2: Voice cloning (disabled - requires too much RAM) ─────────────────
@app.route("/generate", methods=["POST"])
def generate():
    return jsonify({
        "success": False,
        "error": "Voice cloning is currently unavailable. Upgrade to a higher plan to enable it."
    }), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)