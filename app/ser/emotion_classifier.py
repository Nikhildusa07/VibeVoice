import os
import json
import numpy as np
import librosa
import tensorflow as tf

def extract_mfcc(file_path, n_mfcc=13, sr=22050):
    """
    Loads an audio file and extracts MFCC features.
    Averages the MFCCs over time to create a fixed-length feature vector.
    
    Parameters:
        file_path (str): Path to the audio file.
        n_mfcc (int): Number of MFCC coefficients to extract.
        sr (int): Sample rate to use.
    
    Returns:
        numpy.ndarray: A 1D array of averaged MFCC features.
    """
    try:
        audio, sample_rate = librosa.load(file_path, sr=sr, mono=True)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        return mfccs_mean
    except Exception as e:
        print(f"Error extracting MFCC from {file_path}: {e}")
        raise

def load_model_and_metadata():
    """
    Loads the trained model and metadata (label mapping).
    
    Returns:
        model: The loaded Keras model.
        metadata (dict): Mapping of class indices (as strings) to emotion labels.
    """
    model_path = os.path.join("app", "ser", "models", "model.h5")
    metadata_path = os.path.join("app", "ser", "models", "model_metadata.json")
    
    model = tf.keras.models.load_model(model_path)
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    return model, metadata

def predict_emotion(audio_file_path, n_mfcc=13, sr=22050):
    """
    Given an audio file, predicts the emotion using the trained model.
    
    Parameters:
        audio_file_path (str): Path to the input audio file.
        n_mfcc (int): Number of MFCC coefficients (should match training).
        sr (int): Sample rate for audio loading.
        
    Returns:
        str: Predicted emotion label.
    """
    model, metadata = load_model_and_metadata()
    mfcc_features = extract_mfcc(audio_file_path, n_mfcc=n_mfcc, sr=sr)
    mfcc_features = np.expand_dims(mfcc_features, axis=0)  # Add batch dimension
    predictions = model.predict(mfcc_features)
    predicted_index = int(np.argmax(predictions, axis=1)[0])
    predicted_emotion = metadata.get(str(predicted_index), "Unknown")
    return predicted_emotion

if __name__ == "__main__":
    # Set the directory that holds your audio files.
    audio_data_dir = os.path.join("data", "Audio_data")
    
    # Define allowed file extensions
    allowed_extensions = (".wav", ".mp3", ".flac")
    
    # Recursively search for all files with allowed extensions in audio_data_dir.
    audio_files = []
    for root, dirs, files in os.walk(audio_data_dir):
        for file in files:
            if file.lower().endswith(allowed_extensions):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print(f"No audio files found in {os.path.abspath(audio_data_dir)}")
    else:
        # Use the first found audio file as the sample.
        sample_audio_path = audio_files[0]
        print(f"Using sample file: {os.path.abspath(sample_audio_path)}")
        emotion = predict_emotion(sample_audio_path)
        print("Predicted emotion:", emotion)
        
        # Optionally, save the predicted emotion to a text file.
        output_path = os.path.join("data", "predicted_emotion.txt")
        with open(output_path, "w") as f:
            f.write(f"Predicted emotion: {emotion}\n")
        print(f"Prediction saved to: {os.path.abspath(output_path)}")
