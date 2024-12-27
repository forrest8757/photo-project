"""Failures of this code:
    1. if photos have the same name it will erasethe previous one
    Soultion add only 1 folder at a time ...OR... add a unique id to the photo name
"""
import os
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

# Set the path to your "tobesorted" folder
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
tobesorted_path = os.path.join(desktop_path, "tobesorted")

# Ensure the folder exists
os.makedirs(tobesorted_path, exist_ok=True)

@app.route('/')
def index():
    """Render the main page with the drag-and-drop form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads from users on the network."""
    if 'file' not in request.files:
        return {'message': 'No file part in the request'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'message': 'No file selected'}, 400

    # Save the file to the "tobesorted" folder
    save_path = os.path.join(tobesorted_path, file.filename)
    file.save(save_path)
    
    print(f"File saved to {save_path}")
    return {'message': 'File uploaded successfully'}

@app.route('/start-photos', methods=['POST'])
def start_photos():
    """Start the photo sorting process."""
    try:
        subprocess.Popen(['python3', 'photo.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {'message': 'Photo sorting started'}
    except Exception as e:
        return {'message': f'Error starting photo sorting: {e}'}, 500
    
if __name__ == '__main__':
    # Get your computer's local IP so other devices can access it
    from socket import gethostbyname, gethostname
    ip_address = gethostbyname(gethostname())
    print(f"App running at: http://{ip_address}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
