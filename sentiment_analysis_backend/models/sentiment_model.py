from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

class SentimentModel:
    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def train(self, X_train, y_train):
        self.vectorizer = CountVectorizer()
        X_train_counts = self.vectorizer.fit_transform(X_train)
        self.classifier = MultinomialNB()
        self.classifier.fit(X_train_counts, y_train)
        self.save_model()


    def predict(self, text):
        """
        Predicts the sentiment of a given text and provides an explanation.
        """
        if not self.vectorizer or not self.classifier:
            raise RuntimeError("Model is not loaded.")
        text_counts = self.vectorizer.transform([text])
        sentiment = self.classifier.predict(text_counts)[0]
        explanation = self.get_explanation(text_counts)
        return sentiment, explanation

    def get_explanation(self, text_counts):
        """
        Generates an explanation for the predicted sentiment.
        """
        if self.vectorizer is None or self.classifier is None:
            raise RuntimeError("Model is not loaded.")
    
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Verifica si coef_ está disponible
        if hasattr(self.classifier, 'coef_'):
            coefs = self.classifier.coef_.flatten()
            sorted_indices = coefs.argsort()
            top_indices = sorted_indices[-10:]  # Top 10 important features
            top_features = [feature_names[i] for i in top_indices]
            top_coefs = [coefs[i] for i in top_indices]
            explanation = "\n" + "\n".join(
                [f"{feature}: {coef:.2f}" for feature, coef in zip(top_features, top_coefs)]
            )
        else:
            # Alternativa si coef_ no está disponible
            feature_counts = text_counts.toarray().flatten()
            top_indices = feature_counts.argsort()[-10:]  # Top 10 important features
            top_features = [feature_names[i] for i in top_indices]
            explanation = "\n" + ", ".join(top_features)
        
        return explanation



    def save_model(self):
        """
        Saves the trained model to a file.
        """
        with open('models/sentiment_model.pkl', 'wb') as model_file:
            pickle.dump((self.vectorizer, self.classifier), model_file)

    def load_model(self):
        """
        Loads the trained model from a file.
        """
        model_path = 'models/sentiment_model.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model file does not exist.")
        with open(model_path, 'rb') as model_file:
            self.vectorizer, self.classifier = pickle.load(model_file)
