from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image, ImageEnhance, ImageFilter
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
PROCESSED_FOLDER = 'static/processed/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def process_image(input_path, output_path, operation):
    image = Image.open(input_path)

    if operation == 'brightness':
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(2.5)
    elif operation == 'smoothing':
        image = image.filter(ImageFilter.SMOOTH)
    elif operation == 'sharpening':
        image = image.filter(ImageFilter.SHARPEN)
    elif operation == 'blurring':
        image = image.filter(ImageFilter.BLUR)
    elif operation == 'grayscale':
        image = image.convert('L')
    elif operation == 'edge_detection':
            image = image.filter(ImageFilter.FIND_EDGES)
    elif operation == 'crop':
            image = image.crop((0, 0, 300, 300))

    image.save(output_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'operation' not in request.form:
        return redirect(request.url)

    files = request.files.getlist('file')
    operation = request.form['operation']
    processed_paths = []

    operation_folder = os.path.join(app.config['PROCESSED_FOLDER'], operation)
    if not os.path.exists(operation_folder):
        os.makedirs(operation_folder)

    for file in files:
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            processed_filename = f'{operation}_{filename}'
            processed_path = os.path.join(operation_folder, processed_filename)
            process_image(file_path, processed_path, operation)
            processed_paths.append(processed_path)

    return render_template('index.html', processed_paths=processed_paths)

if __name__ == '__main__':
    app.run(debug=True)
