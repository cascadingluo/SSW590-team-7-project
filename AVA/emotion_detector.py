# import os


# if os.environ.get("CI") == "true":
#     class EmotionDetector:
#         def detect_emotion(self, text):
#             return "neutral", 1.0

# else:
#     import tensorflow as tf
#     import numpy as np
#     import pickle
#     from tensorflow.keras.preprocessing.sequence import pad_sequences
#     class EmotionDetector:
#         def __init__(self):
#         # I am loading my trained emotion detection model here
#             self.model = tf.keras.models.load_model('emotion_detection_model.h5')
            
#             # Loading the tokenizer used for training
#             with open('tokenizer.pickle', 'rb') as handle:
#                 self.tokenizer = pickle.load(handle)
            
#             self.emotions = ['anger', 'joy', 'sadness', 'fear', 'love', 'surprise']

#         def preprocess_text(self, text):
#             sequences = self.tokenizer.texts_to_sequences([text])
#             padded_sequences = pad_sequences(sequences, maxlen=100)
#             return padded_sequences
        
#         # Predicts the emotion of the input text.
#         def detect_emotion(self, text):
#             preprocessed_text = self.preprocess_text(text)
#             predictions = self.model.predict(preprocessed_text)
#             predicted_emotion_index = np.argmax(predictions)
#             predicted_emotion = self.emotions[predicted_emotion_index]
#             confidence = predictions[0][predicted_emotion_index]
#             return predicted_emotion, float(confidence)