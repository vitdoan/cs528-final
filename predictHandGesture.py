import os
import pandas as pd
from joblib import load
from featureExtraction import extractFeatures528


def predictHandGesture(file_path):
    # Load the scaler and model
    scaler = load("scaler.joblib")
    clf = load("svm_model.joblib")

    # Read the data file
    try:
        data = pd.read_csv(file_path, header=None, delimiter=",")
        feature = extractFeatures528(data.values, fs=100, numLags=20)
        features_df = pd.DataFrame([feature])
    except Exception as e:
        print(f"Error loading or processing data file: {e}")
        return None

    # Standardize the features
    try:
        X_scaled = scaler.transform(features_df)
    except Exception as e:
        print(f"Error scaling features: {e}")
        return None

    # Predict using the loaded model
    try:
        predicted_label = clf.predict(X_scaled)
        return predicted_label[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None


# Example usage
current_path = os.getcwd()
file_path = os.path.join(current_path, "up_00.txt")
predicted_label = predictHandGesture(file_path)
print("Predicted Label:", predicted_label)
