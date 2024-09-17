from keras.models import load_model
import numpy as np
import os
from scripts.train_model import train_and_save_model
from sklearn.preprocessing import MinMaxScaler


class LSTMModel:
    def __init__(self):
        model_path = 'models/lstm_model.keras'
        if not os.path.isfile(model_path):
            print(f"Model file not found. Training a new model...")
            train_and_save_model()  # Train the model if not found
        self.model = load_model(model_path)

    # Preprocess the data for LSTM
    def preprocess_data(data):
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        prediction_days = 60  # Use the last 60 days to predict the next day
        x_train, y_train = [], []

        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x - prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        return x_train, y_train, scaler

    def predict(self, data):
        """Predict using the LSTM model."""
        processed_data = self.preprocess_data(data)
        prediction = self.model.predict(processed_data)
        return prediction

    # TODO: Implement a decision layer to integrate signals from both the ML model and TA strategies.
