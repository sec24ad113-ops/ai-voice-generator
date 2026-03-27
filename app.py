from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid

app = Flask(__name__)

# 📁 Folders
AUDIO_FOLDER = os.path.join("static", "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# 🎧 Voice files
MY_VOICE = os.path.join("static", "hanirecording.wav")
RAJINI_VOICE = os.path.join("static", "rajini_clean.wav")

# ⚡ Device
device = "cpu"



@app.route("/")
def index():
    return "App is working"


# ── Route 1: Speak in YOUR cloned voice ──────────────────────────────────────
@app.route("/generate", methods=["POST"])
def generate():
    try:
        global tts_clone
        # if tts_clone is None:
        #     tts_clone = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        text = request.form.get("text", "").strip()
        language = request.form.get("language", "en")

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        if not os.path.exists(MY_VOICE):
            return jsonify({"success": False, "error": "Voice file not found"}), 500

        filename = f"speech_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_FOLDER, filename)

        # tts_clone.tts_to_file(
        #     text=text,
        #     speaker_wav=MY_VOICE,
        #     language=language,
            # file_path=output_path
        

        return jsonify({
        "success": True,
        "audio_url": url_for('static', filename=f"audio/{filename}"),
        "message": "TTS Disabled"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── Route 2: Speak in standard AI voice ──────────────────────────────────────
@app.route("/generate-ai", methods=["POST"])
def generate_ai():
    try:
        global tts_ai
        # if tts_ai is None:
        #     tts_ai = TTS("tts_models/en/vctk/vits").to(device)

        text = request.form.get("text", "").strip()

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        filename = f"ai_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_FOLDER, filename)

        # tts_ai.tts_to_file(text=text, speaker="p225", file_path=output_path)

        return jsonify({
            "success": True,
            "audio_url": url_for('static', filename=f"audio/{filename}")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── Route 3: Speak in Rajinikanth's cloned voice ─────────────────────────────
@app.route("/generate-rajini", methods=["POST"])
def generate_rajini():
    try:
        global tts_clone
        # if tts_clone is None:
        #     tts_clone = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        text = request.form.get("text", "").strip()
        language = request.form.get("language", "en")

        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        if not os.path.exists(RAJINI_VOICE):
            return jsonify({"success": False, "error": "Rajini voice file not found"}), 500

        filename = f"rajini_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_FOLDER, filename)

        # tts_clone.tts_to_file(
        #     text=text,
        #     speaker_wav=RAJINI_VOICE,
        #     language=language,
        #     file_path=output_path
    

        return jsonify({
            "success": True,
            "audio_url": url_for('static', filename=f"audio/{filename}")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)