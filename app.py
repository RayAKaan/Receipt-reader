import os
import cv2
import pytesseract
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np

# Set the path to the Tesseract executable (Ensure it's correct)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

# Initialize Flask app
app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a more secure key
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded images
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  # Allowed image file extensions

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to process the receipt image and extract text
def process_receipt_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return ""

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Apply Gaussian blur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding the image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    # Optionally, apply some morphological transformations to remove noise (dilate and erode)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Save the processed image for debugging (optional)
    cv2.imwrite("processed_image.jpg", morph)

    # Perform OCR on the processed image
    custom_config = r'--oem 3 --psm 6'  # Update if needed
    text = pytesseract.image_to_string(morph, lang='eng', config=custom_config)

    # Print the extracted text for debugging
    print("Extracted Text:")
    print(text)

    return text

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading receipt
@app.route('/upload', methods=['POST'])
def upload_receipt():
    if 'receipt' not in request.files:
        flash("No file part", 'error')
        return redirect(request.url)

    file = request.files['receipt']
    if file.filename == '':
        flash("No selected file", 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Save the uploaded image to a temporary file
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # Process the image to extract text
        extracted_text = process_receipt_image(image_path)

        # Display the extracted text in the UI
        flash(f"Extracted Text: {extracted_text}", 'success')

        return render_template('index.html')

    flash("Invalid file format", 'error')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
