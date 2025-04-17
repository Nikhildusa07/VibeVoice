import os
import librosa
import soundfile as sf

# Define the source directory containing raw audio
raw_audio_dir = os.path.join("data", "Audio_data")
print("Raw audio directory:", os.path.abspath(raw_audio_dir))

# Define the target directory to save processed audio
processed_audio_dir = os.path.join("data", "processed_audio")
print("Processed audio directory:", os.path.abspath(processed_audio_dir))
os.makedirs(processed_audio_dir, exist_ok=True)

# Target sample rate for processing (e.g., 22050 Hz)
TARGET_SR = 22050

files_processed = 0

# Walk through all files in the raw audio directory
for root, dirs, files in os.walk(raw_audio_dir):
    for file in files:
        # Process only audio files (e.g., .wav, .mp3, .flac)
        if file.lower().endswith((".wav", ".mp3", ".flac")):
            file_path = os.path.join(root, file)
            print("Processing file:", os.path.abspath(file_path))
            try:
                # Load the audio file with the target sample rate
                audio, sr = librosa.load(file_path, sr=TARGET_SR, mono=True)
                # Trim silence from the beginning and end of the clip
                audio_trimmed, _ = librosa.effects.trim(audio)
                
                # Preserve subfolder structure by calculating the relative path
                relative_path = os.path.relpath(root, raw_audio_dir)
                save_dir = os.path.join(processed_audio_dir, relative_path)
                os.makedirs(save_dir, exist_ok=True)
                
                # Define the new file path in the processed directory
                new_file_path = os.path.join(save_dir, file)
                
                # Save the processed audio file using soundfile
                sf.write(new_file_path, audio_trimmed, TARGET_SR)
                print(f"Processed and saved: {os.path.abspath(new_file_path)}")
                files_processed += 1
            except Exception as e:
                print(f"Failed to process {os.path.abspath(file_path)}: {e}")

if files_processed == 0:
    print("No audio files were processed. Please check the raw audio folder and file extensions.")
else:
    print(f"Audio preprocessing completed. {files_processed} file(s) processed.")
