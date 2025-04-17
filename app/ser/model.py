import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization, Activation
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical

def extract_emotion_label(file_path):
    """
    Extracts the emotion label from a RAVDESS file name.
    RAVDESS file names are typically formatted like: "03-01-08-01-01-02-24.wav"
    where the third token (e.g., "08") represents the emotion code.
    
    The following mapping is commonly used for RAVDESS:
        "01": "neutral",
        "02": "calm",
        "03": "happy",
        "04": "sad",
        "05": "angry",
        "06": "fearful",
        "07": "disgust",
        "08": "surprised"
    
    If the file name does not follow this convention, "unknown" is returned.
    """
    base_name = os.path.basename(file_path)
    parts = base_name.split('-')
    if len(parts) >= 3:
        emotion_code = parts[2]
        emotion_mapping = {
            "01": "neutral",
            "02": "calm",
            "03": "happy",
            "04": "sad",
            "05": "angry",
            "06": "fearful",
            "07": "disgust",
            "08": "surprised"
        }
        return emotion_mapping.get(emotion_code, "unknown")
    return "unknown"

# Load features CSV generated from feature_extraction.py
features_csv = os.path.join("data", "features.csv")
df = pd.read_csv(features_csv)

# Ensure the CSV has a column with file paths for label extraction.
if "file" not in df.columns:
    raise Exception("The features CSV must contain a 'file' column for label extraction.")

# Assume that feature columns are all columns except "file".
feature_columns = df.columns[:-1]
X = df[feature_columns].values

# Extract labels from the file names using the extraction function.
df['label'] = df['file'].apply(extract_emotion_label)
y_labels = df['label'].values

# Filter out samples with "unknown" label.
valid_indices = [i for i, label in enumerate(y_labels) if label != "unknown"]
if not valid_indices:
    raise Exception("No valid emotion labels found in the dataset.")

X = X[valid_indices]
y_labels = [y_labels[i] for i in valid_indices]

# Encode the string labels into integers.
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_labels)
# Convert to one-hot encoding.
y = to_categorical(y_encoded)

# Save label mapping (metadata) for later use.
label_mapping = {str(index): label for index, label in enumerate(label_encoder.classes_)}
models_dir = os.path.join("app", "ser", "models")
os.makedirs(models_dir, exist_ok=True)
metadata_path = os.path.join(models_dir, "model_metadata.json")
with open(metadata_path, "w") as f:
    json.dump(label_mapping, f, indent=4)
print("Model metadata saved to:", os.path.abspath(metadata_path))

# Split data into training and validation sets (80% training, 20% validation).
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training set shape:", X_train.shape, y_train.shape)
print("Validation set shape:", X_val.shape, y_val.shape)

# Reshape the data for CNN: Assuming 1D features (e.g., MFCCs) → reshape to (samples, time_steps, features)
X_train = X_train[..., np.newaxis]  # Expanding dimensions for Conv1D
X_val = X_val[..., np.newaxis]

# Build a CNN-based model.
model = Sequential()
# First convolutional layer
model.add(Conv1D(64, kernel_size=5, strides=1, padding="same", activation="relu", input_shape=(X_train.shape[1], 1)))
model.add(BatchNormalization())
model.add(MaxPooling1D(pool_size=2))

# Second convolutional layer
model.add(Conv1D(128, kernel_size=3, strides=1, padding="same", activation="relu"))
model.add(BatchNormalization())
model.add(MaxPooling1D(pool_size=2))

# Third convolutional layer
model.add(Conv1D(256, kernel_size=3, strides=1, padding="same", activation="relu"))
model.add(BatchNormalization())
model.add(MaxPooling1D(pool_size=2))

# Flatten and fully connected layers
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(y.shape[1], activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

# Set up callbacks.
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

# Train the model.
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=32,
    callbacks=[early_stop, reduce_lr],
    verbose=1
)

# Evaluate the model on the validation set.
loss, accuracy = model.evaluate(X_val, y_val, verbose=0)
print(f"Validation Accuracy: {accuracy * 100:.2f}%")

# Save the trained model.
model_path = os.path.join(models_dir, "model.h5")
model.save(model_path)
print("Model saved to:", os.path.abspath(model_path))
