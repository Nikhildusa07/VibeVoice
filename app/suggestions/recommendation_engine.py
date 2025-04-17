import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.suggestions.activity_mapping import map_emotion_to_activities

#from app.suggestions.activity_mapping import map_emotion_to_activities

class RecommendationEngine:
    """
    A simple recommendation engine that returns activity suggestions
    based on a detected emotion.
    """
    def get_suggestions(self, emotion):
        """
        Get activity suggestions for the given emotion.
        
        Args:
            emotion (str): The detected emotion.
            
        Returns:
            list: A list of suggested activities.
        """
        return map_emotion_to_activities(emotion)

# Test the recommendation engine if this file is run directly.
if __name__ == "__main__":
    engine = RecommendationEngine()
    test_emotions = [
        "happy", "sad", "angry", "neutral", 
        "calm", "fearful", "disgust", "surprised", 
        "unknown"
    ]
    for emotion in test_emotions:
        suggestions = engine.get_suggestions(emotion)
        print(f"Emotion: {emotion} -> Suggestions: {suggestions}")
