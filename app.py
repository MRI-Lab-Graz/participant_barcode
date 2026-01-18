import os
import sys
import webbrowser
import threading
import socket
import shutil
import re
from flask import Flask, render_template, jsonify, request, send_file
from waitress import serve

# Add root directory to path to import pdf_generator
if hasattr(sys, '_MEIPASS'):
    # In PyInstaller bundle, the root is _MEIPASS
    sys.path.append(sys._MEIPASS)
else:
    # In development, the root is the current file's directory
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pdf_generator import generate_pdfs

app = Flask(__name__)

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# Update Flask template and static folders for PyInstaller
if hasattr(sys, '_MEIPASS'):
    app.template_folder = os.path.join(sys._MEIPASS, 'templates')
    app.static_folder = os.path.join(sys._MEIPASS, 'static')

# Basic Routes
@app.route('/')
def index():
    # List templates in subject_info
    template_dir = get_resource_path('subject_info')
    
    templates = [f for f in os.listdir(template_dir) if f.endswith('.tex')]
    
    # List existing output folders
    # For output, we always want the current working directory, not the bundle dir
    output_base = os.path.join(os.getcwd(), 'generated_pdfs')
    if not os.path.exists(output_base):
        os.makedirs(output_base)
    
    output_folders = [f for f in os.listdir(output_base) if os.path.isdir(os.path.join(output_base, f))]
    
    return render_template('index.html', templates=templates, output_folders=output_folders)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form
    template_name = data.get('template')
    barcode_input = data.get('barcodes', '')
    barcode_file = request.files.get('barcode_file')
    output_folder_name = data.get('output_folder', 'default')
    just_download = data.get('just_download') == 'true'

    # Get barcode list
    codes = []
    if barcode_file and barcode_file.filename:
        codes = [line.decode('utf-8').strip() for line in barcode_file.readlines() if line.strip()]
    elif barcode_input:
        codes = [line.strip() for line in barcode_input.split('\n') if line.strip()]

    if not codes:
        return jsonify(success=False, message="No barcodes provided.")

    # Validation: No spaces, no special chars, no Umlaute
    valid_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
    invalid_codes = [c for c in codes if not valid_pattern.match(c)]
    if invalid_codes:
        return jsonify(success=False, message=f"Invalid characters found in codes: {', '.join(invalid_codes)}. No spaces, Umlaute or specific special characters allowed.")

    # Validation: Uniqueness
    seen = set()
    duplicates = set()
    for c in codes:
        if c in seen:
            duplicates.add(c)
        seen.add(c)
    if duplicates:
        return jsonify(success=False, message=f"Duplicate IDs found: {', '.join(duplicates)}")

    # Paths
    template_path = os.path.join(get_resource_path('subject_info'), template_name)
    
    # We use current working directory for user files (barcodes, outputs)
    working_dir = os.getcwd()
    
    if just_download:
        output_dir = os.path.join(working_dir, 'temp_output')
    else:
        output_dir = os.path.join(working_dir, 'generated_pdfs', output_folder_name)

    # Generate
    results = generate_pdfs(codes, template_path, output_dir, barcode_dir=os.path.join(working_dir, 'barcodes'))

    if just_download:
        # Create a ZIP of the generated PDFs
        zip_path = os.path.join(working_dir, 'generated_barcodes.zip')
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', output_dir)
        # Clean up temp output
        shutil.rmtree(output_dir)
        return send_file(zip_path, as_attachment=True)

    return jsonify(success=True, results=results)

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.json.get('name')
    if not folder_name:
        return jsonify(success=False, message="No folder name provided.")
    
    output_base = os.path.join(os.getcwd(), 'generated_pdfs')
    new_folder_path = os.path.join(output_base, folder_name)
    
    try:
        os.makedirs(new_folder_path, exist_ok=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the Flask server after a short delay to allow response to send."""
    print("Shutdown requested...")
    def kill_server():
        threading.Timer(0.5, lambda: os._exit(0)).start()
    
    kill_server()
    return jsonify(success=True)

def find_free_port(host='127.0.0.1'):
    """Find a free port on specified host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]

def open_browser(url):
    """Wait for server to start and then open the browser."""
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()

if __name__ == '__main__':
    # Configuration
    host = '127.0.0.1'
    port = 5001
    
    # Check if preferred port is free
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex((host, port)) == 0:
            print(f" * Port {port} is in use, finding a free port...")
            port = find_free_port(host)

    url = f'http://{host}:{port}'
    print(f" * Starting server at {url}")
    
    # Open browser in a separate thread
    open_browser(url)
    
    # Run with Waitress
    try:
        serve(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
