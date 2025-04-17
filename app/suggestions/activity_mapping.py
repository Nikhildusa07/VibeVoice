def map_emotion_to_activities(emotion):
    """
    Maps a given emotion to a list of recommended activities.
    
    Args:
        emotion (str): The detected emotion (e.g., "happy", "sad", "angry", etc.)
    
    Returns:
        list: A list of activity suggestions tailored to that emotion.
    """
    mapping = {
        "happy": [
            "Share your joy on social media",
            "Plan a fun outing with friends",
            "Celebrate your happiness with your favorite song"
        ],
        "sad": [
            "Listen to uplifting music",
            "Watch a lighthearted movie",
            "Call a friend or family member for support"
        ],
        "angry": [
             "Listen to calming music",
             "Take a brisk walk to cool down",
             "Practice deep breathing or meditation"
        ],
        "neutral": [
            "Try a new hobby",
            "Read a book or article",
            "Explore a new place in your city"
        ],
        "calm": [
            
            "Meditate or practice yoga",
            "Take a leisurely walk in nature",
            "Enjoy a quiet activity like reading or drawing"
        ],
        "fearful": [
            "Practice mindfulness or meditation",
            "Talk to someone you trust about your feelings",
            "Engage in a relaxing activity like listening to soft music"
        ],
        "disgust": [
            "Talk with a friend or loved one",
            "Watch a funny video to lighten your mood",
            "Do something you love to distract yourself"
            
        ],
        "surprised": [
            
            "Share your excitement with someone",
            "Explore an interesting topic or activity",
            "Embrace the unexpected—try something new"
        ],
        # Fallback for any unrecognized emotion:
        "unknown": [
            "Reach out to a friend",
            "Take some time to relax",
            "Do an activity you enjoy"
            
        ]
    }
    
    # Return the suggestions for the given emotion (case-insensitive),
    # or default to "unknown" if not found.
    return mapping.get(emotion.lower(), mapping["unknown"])

# Test the mapping if this file is run directly.
if __name__ == "__main__":
    test_emotions = [
        "happy", "sad", "angry", "neutral", 
        "calm", "fearful", "disgust", "surprised", 
        "unknown", "confused"
    ]
    for emotion in test_emotions:
        suggestions = map_emotion_to_activities(emotion)
        print(f"Emotion: {emotion} -> Suggestions: {suggestions}")
