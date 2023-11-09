import os
import configparser
import hashlib
from flask import Flask, render_template, request, session, jsonify
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
        config['DEFAULT']['password'] = hashlib.md5(password.encode('utf-8')).hexdigest()  # Using MD5 for hashing
        config['DEFAULT']['download_location'] = download_location
        config['DEFAULT']['quality'] = str(quality)
        with open(config_file, 'w') as f:
            config.write(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Create a config file on first use
    create_or_update_config(None, None, None, None, create=True)
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        url = request.form['url']
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
            qobuz.handle_url(url)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return jsonify(status='error', message=str(e)), 500

        if request.form.get('remember') == 'on':
            # Save the settings in the config file
            create_or_update_config(email, password, request.form['download_location'], request.form['quality'])

        return jsonify(status='completed')

    # Pre-fill the form with values from config if it exists
    config = configparser.ConfigParser()
    config.read(config_file)
    email = config['DEFAULT'].get('email', '')
    download_location = config['DEFAULT'].get('download_location', '')
    quality = config['DEFAULT'].get('quality', '7')
    
    return render_template('index.html', email=email, download_location=download_location, quality=quality)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
