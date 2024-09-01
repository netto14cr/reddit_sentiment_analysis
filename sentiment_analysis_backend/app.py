import platform
from flask import Flask, render_template,request,session,url_for,redirect,flash
from flask_cors import CORS
from routes.api_routes import api_blueprint
from dotenv import load_dotenv
import os
import logging
import json
import re
import webbrowser
import threading


# Load environment variables from .env file
load_dotenv()

# Read CORS origins from environment variable and convert to list
cors_origins = os.getenv('CORS_ORIGINS', '').split(',')

app = Flask(__name__)
CORS(app, origins=cors_origins)  # Enable CORS for all routes
app.secret_key = 'your_secret_key_here'


# Configure the logging module
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')


@app.route('/')
def index():
    return render_template('main/index.html')

def read_log_data():
    log_entries = []
    search_query_pattern = re.compile(r'Search Query: (.+)')
    title_pattern = re.compile(r'Post Title: (.+)')
    sentiment_pattern = re.compile(r'Sentiment: (.+)')
    explanation_pattern = re.compile(r'Explanation: (.+)')
    
    if os.path.exists('app.log'):
        with open('app.log', 'r', encoding='latin1') as file:
            lines = file.readlines()
            for line in lines:
                search_query_match = search_query_pattern.search(line)
                title_match = title_pattern.search(line)
                sentiment_match = sentiment_pattern.search(line)
                
                if search_query_match and title_match and sentiment_match:
                    log_entries.append({
                        'search_query': search_query_match.group(1),
                        'title': title_match.group(1),
                        'sentiment': sentiment_match.group(1)
                    })
    return log_entries



@app.route('/search_results')
def search_results():
    log_data = read_log_data()
    
    # Use a dictionary to store unique search queries
    unique_results = {}
    for entry in log_data:
        # Split the search query by the first hyphen and use the first part
        search_query = entry['search_query'].split(' - ')[0]
        
        if search_query not in unique_results:
            unique_results[search_query] = entry  # Store the first entry found
    
    # Dictionary comprehension to format the results
    # For each search query, store the entry in a list
    results = {term: [entry] for term, entry in unique_results.items()}
    
    return render_template('data/search_results.html', results=results)




@app.route('/view_details/<search_query>')
def view_details(search_query):
    log_data = read_log_data()
    
    # Clean the search query by removing the extra information
    search_query_cleaned = search_query.split(' - ')[0].strip()
    
    # Function to extract the value from the field
    def extract_value(field):
        return field.split(':')[1] if ':' in field else field
    
    # Filter the log data based on the search query
    filtered_data = []
    for index, entry in enumerate(log_data):
        # Split the search query by the first hyphen
        query_parts = entry['search_query'].split(' - ')
        # Verify if the first part of the query matches the cleaned search query
        if query_parts[0].strip() == search_query_cleaned:
            # Verify if the query has more than one part
            title = query_parts[1].strip() if len(query_parts) > 1 else ''
            sentiment = query_parts[2].strip() if len(query_parts) > 2 else ''
            explanation = query_parts[3].strip() if len(query_parts) > 3 else ''
            
            # Extract the values from the fields
            title=extract_value(title)
            sentiment=extract_value(sentiment)
            explanation=extract_value(explanation)
            
            # Add the filtered data to the list
            filtered_data.append({
                'result_number': index + 1, 
                'search_query': query_parts[0].strip(),  # Here we use the original search query
                'post_title': title,
                'sentiment': sentiment,
                'explanation': explanation
            })
    
    return render_template('data/view_details.html', search_query=search_query, details=filtered_data)




@app.route('/admin/system_info')
def system_info():
    system_info_data = {
        "System": platform.system(),
        "Node": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }
    return render_template('admin/system_info.html', system_info=system_info_data)

@app.route('/admin/env_vars')
def env_vars():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    env_vars = {}

    # Check if the .env file exists
    if os.path.exists(env_file):
        # Read the .env file to get all the variables
        with open(env_file) as f:
            for line in f:
                if line.strip():
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value

    # Ensure that required environment variables are in the dictionary
    important_env_vars = {
        "REDDIT_CLIENT_ID": env_vars.get("REDDIT_CLIENT_ID", ""),
        "REDDIT_CLIENT_SECRET": env_vars.get("REDDIT_CLIENT_SECRET", ""),
        "REDDIT_USER_AGENT": env_vars.get("REDDIT_USER_AGENT", ""),
        "URL": env_vars.get("URL", ""),
        "PORT": env_vars.get("PORT", ""),
        "PROTOCOL": env_vars.get("PROTOCOL", ""),
        "FLASK_ENV": env_vars.get("FLASK_ENV", ""),
    }

    # If no variables were loaded, provide an error message
    if not env_vars:
        error_message = "The .env file was not found, this functionality is not available in production servers, only in development environments."
    else:
        error_message = None

    return render_template('admin/env_vars.html',
                           env_vars=important_env_vars,
                           error_message=error_message)



@app.route('/admin/edit_env_vars', methods=['GET', 'POST'])
def edit_env_vars():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    # Leer el archivo .env para obtener todas las variables
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=', 1)
                env_vars[key] = value

    if request.method == 'POST':
        # Actualizar todas las variables en el archivo .env
        for key in env_vars.keys():
            # Obtén el nuevo valor del formulario o deja el actual si no se proporciona
            new_value = request.form.get(key, env_vars[key])
            env_vars[key] = new_value
        
        # Escribir los valores actualizados en el archivo .env
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        flash("Environment variables updated successfully!", "success")
        return redirect(url_for('env_vars'))

    return render_template('admin/edit_env_vars.html', env_vars=env_vars)



@app.route('/admin/save_env_vars', methods=['POST'])
def save_env_vars():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    env_vars = {
        "REDDIT_CLIENT_ID": request.form.get("REDDIT_CLIENT_ID"),
        "REDDIT_CLIENT_SECRET": request.form.get("REDDIT_CLIENT_SECRET"),
        "REDDIT_USER_AGENT": request.form.get("REDDIT_USER_AGENT"),
        "URL": request.form.get("URL"),
        "PORT": request.form.get("PORT"),
        "PROTOCOL": request.form.get("PROTOCOL"),
        "FLASK_ENV": request.form.get("FLASK_ENV"),
    }
    
    with open(env_file, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    flash("Environment variables updated successfully!", "success")
    return redirect(url_for('env_vars'))


def open_browser(url, port, protocol):
    full_url = f"{protocol}://{url}:{port}"
    webbrowser.open(full_url)

if __name__ == '__main__':
    URL = os.getenv("URL", "127.0.0.1")  # Default url value if not provided
    PORT = int(os.getenv("PORT", 5000))  # Default port value if not provided
    # Get the boolean value from the environment variable
    FLASK_ENV = os.getenv("FLASK_ENV", "False").lower() == "true"  # Convert to boolean
    PROTOCOL = os.getenv("PROTOCOL", "http")  # Add a new environment variable for the protocol
    
    # Verify if the server is not in debug mode
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        # Open the browser in a separate thread
        threading.Timer(2, open_browser, args=[URL, PORT, PROTOCOL]).start()  # Pasar protocolo como argumento
    
    # Run the Flask app with the provided configuration
    app.run(host=URL, port=PORT, debug=FLASK_ENV, use_reloader=FLASK_ENV)