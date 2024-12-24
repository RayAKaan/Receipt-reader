from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import cv2
import pytesseract

# Explicitly specify the Tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'your_secret_key'  # Ensure this is a secret key for flash messages

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload receipt
@app.route('/', methods=['GET', 'POST'])
def upload_receipt():
    if request.method == 'POST':
        if 'receipt' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['receipt']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extracted_text = process_receipt_image(filename)
            flash('Receipt uploaded successfully', 'success')
            return render_template('index.html', extracted_text=extracted_text)
        else:
            flash('Invalid file format. Please upload a valid image.', 'error')
            return redirect(request.url)
    return render_template('index.html')

# Function to process the uploaded receipt image and extract text using Tesseract
def process_receipt_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Optional: Apply thresholding for better results
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # Use pytesseract to extract text
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(thresh, config=custom_config)
    return extracted_text

# Route to view all receipts
@app.route('/view_receipts')
def view_receipts():
    receipts = get_all_receipts()  # This can be from your database or folder
    return render_template('view_receipts.html', receipts=receipts)

# Function to get all receipts (replace with actual logic)
def get_all_receipts():
    # In a real-world scenario, you might pull this from a database.
    # For simplicity, we'll list the files in the 'uploads' folder.
    receipt_files = os.listdir(app.config['UPLOAD_FOLDER'])
    receipts = []
    for receipt in receipt_files:
        if allowed_file(receipt):
            receipts.append({
                'filename': receipt,
                'uploaded_on': '2024-12-24'  # Replace with actual timestamp
            })
    return receipts

# Route to export receipts to PDF (this is a placeholder)
@app.route('/export_pdf')
def export_pdf():
    # Implement PDF export functionality here
    flash('Exported to PDF (Feature coming soon)', 'info')
    return redirect(url_for('upload_receipt'))

if __name__ == '__main__':
    app.run(debug=True)
