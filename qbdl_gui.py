import os
import configparser
import hashlib
from flask import Flask, render_template, request, jsonify
import logging
from qobuz_dl import QobuzDL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'
config_directory = '/app/config'
config_file = os.path.join(config_directory, 'config.ini')  # Updated path to the config file

def create_or_update_config(email, password, download_location, quality, create=False):
    """Create a new config file or update the existing one with the user's settings."""
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)  # Ensure the config directory exists
    config = configparser.ConfigParser()
    if create or not os.path.exists(config_file):
        config['DEFAULT'] = {
            'email': '',
            'password': '',
            'download_location': '',
            'quality': '27',  # Default quality
        }
        with open(config_file, 'w') as f:
            config.write(f)

    if not create:
        config.read(config_file)
        config['DEFAULT']['email'] = email
        config['DEFAULT']['password'] = password  # Store password without hashing
        config['DEFAULT']['download_location'] = download_location
        config['DEFAULT']['quality'] = str(quality)
        with open(config_file, 'w') as f:
            config.write(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        urls = request.form.getlist('url')  # Get list of URLs
        download_location = request.form['download_location']
        quality = int(request.form['quality'])
        remember = request.form.get('rememberMe')

        try:
            qobuz = QobuzDL(
                directory=download_location,
                quality=quality
            )
            qobuz.get_tokens()
            qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)
            for url in urls:  # Handle each URL
                qobuz.handle_url(url)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return jsonify(status='error', message=str(e)), 500

        if remember == 'on':
            # Save the settings in the config file
            create_or_update_config(email, password, download_location, quality)

        return jsonify(status='completed')

    # Pre-fill the form with values from config if it exists
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        email = config['DEFAULT'].get('email', '')
        password = config['DEFAULT'].get('password', '')  # Retrieve password
        download_location = config['DEFAULT'].get('download_location', '')
        quality = config['DEFAULT'].get('quality', '7')
    
    return render_template('index.html', email=email, password=password, download_location=download_location, quality=quality)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    item_type = request.args.get('type')
    qobuz = QobuzDL()  # Initialize QobuzDL
    qobuz.get_tokens()

    # Pre-fill the form with values from config if it exists
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        email = config['DEFAULT'].get('email', '')
        password = config['DEFAULT'].get('password', '')  # Retrieve password

    qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)
    results = qobuz.search_by_type(query, item_type, 10)  # Search using the query and item type
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
