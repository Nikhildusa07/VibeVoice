import sys
import os
import time
from flask import Flask, request, jsonify, send_from_directory
from pydub import AudioSegment

# Add the root directory of the project to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Uncomment and update these lines if ffmpeg/ffprobe are not in your PATH.
# AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
# AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

from app.ser.emotion_classifier import predict_emotion
from app.suggestions.recommendation_engine import RecommendationEngine

def remove_file_safely(file_path, retries=5, delay=1):
    """
    Attempts to remove a file, retrying if a PermissionError occurs.
    Returns True if successful, False otherwise.
    """
    for i in range(retries):
        try:
            os.remove(file_path)
            return True
        except PermissionError:
            time.sleep(delay)
    # Final attempt
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print("Error removing file:", file_path, e)
        return False

# Get the absolute path to the UI folder (located in app/ui/)
current_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(current_dir, "ui")

app = Flask(__name__, static_folder=ui_dir, static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "ui.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']

    # Create a temporary file path for the uploaded file.
    temp_dir = os.path.join("data")
    os.makedirs(temp_dir, exist_ok=True)
    original_ext = os.path.splitext(audio_file.filename)[1]  # e.g., ".webm", ".mp3", ".wav"
    temp_file_path = os.path.join(temp_dir, "temp_audio" + original_ext)
    
    # Save the uploaded file to the temporary location.
    audio_file.save(temp_file_path)

    # Convert the uploaded file to WAV format using pydub.
    temp_wav_path = os.path.join(temp_dir, "temp_audio_converted.wav")
    try:
        audio = AudioSegment.from_file(temp_file_path)
        audio.export(temp_wav_path, format="wav")
    except Exception as e:
        if os.path.exists(temp_file_path):
            remove_file_safely(temp_file_path)
        return jsonify({"error": "Failed to convert audio file to WAV: " + str(e)}), 500

    # Use the converted WAV file for emotion prediction.
    try:
        emotion = predict_emotion(temp_wav_path)
        engine = RecommendationEngine()
        suggestions = engine.get_suggestions(emotion)
        response = {
            "emotion": emotion,
            "suggestions": suggestions
        }
    except Exception as e:
        response = {"error": "An error occurred while predicting emotion: " + str(e)}
    finally:
        # Wait a bit longer to ensure that file handles are released.
        time.sleep(3)
        remove_file_safely(temp_file_path)
        remove_file_safely(temp_wav_path)
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
