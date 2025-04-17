from flask import Flask, request, jsonify, send_from_directory
import os
from ser.emotion_classifier import predict_emotion
from suggestions.recommendation_engine import RecommendationEngine

app = Flask(__name__, static_folder="app/ui", static_url_path="")

@app.route("/")
def index():
    return send_from_directory("app/ui", "ui.html")

# Endpoint for predicting emotion from an uploaded audio file.
@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided.'}), 400

    audio_file = request.files['audio']
    
    # Save the uploaded file temporarily
    temp_path = os.path.join("data", "temp_audio.wav")
    audio_file.save(temp_path)
    
    try:
        # Use your SER module to predict emotion
        emotion = predict_emotion(temp_path)
        # Use your recommendation engine to get suggestions
        engine = RecommendationEngine()
        suggestions = engine.get_suggestions(emotion)
        
        response = {
            "emotion": emotion,
            "suggestions": suggestions
        }
    except Exception as e:
        response = {"error": str(e)}
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
