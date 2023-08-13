# qbdl-gui

qbdl-gui is a gui for qobuz-dl a tool used for downloading music from Qobuz.

## Features

- Download albums, tracks, artists, and playlists from Qobuz.
- Supports various quality levels.
- Embed album art into files.
- Web GUI for easy interaction.

## Installation

1. Clone the repository:

```
git clone https://github.com/konzepts/qbdl-gui.git
```

2. Virtual Environment: Consider using a virtual environment to isolate the dependencies for your project. This can help avoid conflicts between different versions of libraries. You can create a virtual environment using:

```
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

Refer to the existing documentation for command-line usage.

### Web GUI

To use the web GUI, follow these steps:

1. Run the web GUI script:
```
python3 qbdl_gui.py
```
2. Open a web browser and navigate to:

```
http://0.0.0.0:5000/
```
```
localhost:5000
```

3. Enter your Qobuz email, password, download URL, download location, and quality.
4. Click the "Download" button to start the download.

## Contributing

Please refer to the existing guidelines for contributing to this project.

