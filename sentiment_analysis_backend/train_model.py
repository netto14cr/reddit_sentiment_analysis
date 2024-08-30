from models.sentiment_model import SentimentModel

# Prueba con datos de ejemplo
X_train = [
    "I love this product", 
    "Terrible experience, I wouldn't recommend it", 
    "It's a good product, but it could be better", 
    "The worst customer service I've ever had"
]
y_train = ["positive", "negative", "neutral", "negative"]

# Entrenar el modelo
model = SentimentModel()
model.train(X_train, y_train)

# Realizar una predicción y obtener una explicación
text = "I love this product"
text_counts = model.vectorizer.transform([text])
sentiment, explanation = model.predict(text)
print("Sentiment:", sentiment)
print("Explanation:", explanation)
