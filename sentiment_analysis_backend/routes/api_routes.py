from flask import Blueprint, request, jsonify
import praw
from models.sentiment_model import SentimentModel
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Cargar las variables de entorno

api_blueprint = Blueprint('api', __name__)

# Configuración de Reddit API
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Inicializar la instancia de Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Instanciar el modelo de análisis de sentimientos
sentiment_model = SentimentModel()
sentiment_model.load_model()  # Cargar el modelo si está disponible

@api_blueprint.route('/search', methods=['POST'])
def search_posts():
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        # Registrar la búsqueda
        logging.info(f'Search Query: {query}')
        
        # Search for posts in all subreddits
        submissions = reddit.subreddit('all').search(query, limit=5000)
        results = []
        for submission in submissions:
            sentiment, explanation = sentiment_model.predict(submission.title)
            
            # Registrar el análisis de sentimientos
            logging.info(f'Search Query: {query} - Post Title: {submission.title} - Sentiment: {sentiment} - Explanation: {explanation}')
            
            results.append({
                'title': submission.title,
                'sentiment': sentiment,
                'sentiment_explanation': explanation,
                'url': f"https://www.reddit.com{submission.permalink}"
            })
        return jsonify(results)
    except Exception as e:
        # Registrar errores
        logging.error(f'Error occurred: {str(e)}')
        return jsonify({'error': str(e)}), 500
