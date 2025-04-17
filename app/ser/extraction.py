import os
import numpy as np
import librosa
import pandas as pd

def extract_mfcc(file_path, n_mfcc=13, sr=22050):
    """
    Load an audio file and extract its MFCC features.

    Parameters:
        file_path (str): Path to the audio file.
        n_mfcc (int): Number of MFCC coefficients to extract.
        sr (int): Sample rate for loading the audio.

    Returns:
        numpy.ndarray: A fixed-length vector (mean of MFCCs over time).
    """
    try:
        # Load the audio file
        audio, sample_rate = librosa.load(file_path, sr=sr)
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
        # Compute the mean of the MFCCs across the time axis for a fixed-length feature vector
        mfccs_mean = np.mean(mfccs, axis=1)
        return mfccs_mean
    except Exception as e:
        print(f"Error extracting MFCC from {file_path}: {e}")
        raise

def process_all_audio(audio_dir, n_mfcc=13, sr=22050):
    """
    Process all audio files in the specified directory and extract MFCC features.

    Parameters:
        audio_dir (str): Directory containing processed audio files.
        n_mfcc (int): Number of MFCC coefficients to extract.
        sr (int): Sample rate for loading the audio.

    Returns:
        (list, list): A tuple with two lists:
                      - file_paths: paths of processed audio files.
                      - features: extracted feature vectors for each file.
    """
    features = []
    file_paths = []
    # Walk through all files in the audio directory
    for root, dirs, files in os.walk(audio_dir):
        for file in files:
            # Only process audio files with common audio extensions
            if file.lower().endswith((".wav", ".mp3", ".flac")):
                file_path = os.path.join(root, file)
                try:
                    mfcc_feat = extract_mfcc(file_path, n_mfcc=n_mfcc, sr=sr)
                    features.append(mfcc_feat)
                    file_paths.append(file_path)
                    print(f"Extracted features from: {os.path.abspath(file_path)}")
                except Exception as e:
                    print(f"Failed to process {os.path.abspath(file_path)}: {e}")
    return file_paths, features

if __name__ == '__main__':
    # Define the directory containing preprocessed audio files.
    # Make sure that your processed audio files are stored in this directory.
    processed_audio_dir = os.path.join("data", "processed_audio")
    print("Processing audio files in:", os.path.abspath(processed_audio_dir))
    
    # Extract features from all processed audio files
    file_paths, features = process_all_audio(processed_audio_dir)
    
    # If features were extracted, save them to a CSV file for later use.
    if features:
        # Create a DataFrame from the features list.
        # Each row corresponds to a file, and each column corresponds to one MFCC coefficient.
        features_df = pd.DataFrame(features)
        # Add the file path as a column for reference.
        features_df["file"] = file_paths

        # Define the output CSV path (e.g., data/features.csv)
        output_csv_path = os.path.join("data", "features.csv")
        features_df.to_csv(output_csv_path, index=False)
        print(f"Features successfully saved to: {os.path.abspath(output_csv_path)}")
    else:
        print("No features extracted. Please check your processed audio directory.")
