from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pytesseract
from PIL import Image
import cv2
import sqlite3

# Explicitly specify the Tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'your_secret_key'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize SQLite database
DATABASE = 'database/receipts.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            extracted_text TEXT,
            total_expense REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Accessing register route")  # Debug statement
    if request.method == 'POST':
        print("Processing POST request")  # Debug statement
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DATABASE)
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'error')
        finally:
            conn.close()
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # Index 2 for password
            session['user_id'] = user[0]  # Index 0 for user ID
            session['username'] = user[1]  # Index 1 for username
            flash('Login successful!', 'success')
            return redirect(url_for('upload_receipt'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route to upload receipt
@app.route('/', methods=['GET', 'POST'])
def upload_receipt():
    if 'user_id' not in session:
        flash('Please log in to upload receipts.', 'warning')
        return redirect(url_for('login'))

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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            extracted_text, total_expense = process_receipt_image(filepath)

            # Save receipt to the database
            conn = sqlite3.connect(DATABASE)
            conn.execute(
                'INSERT INTO receipts (filename, extracted_text, total_expense, user_id) VALUES (?, ?, ?, ?)',
                (filename, extracted_text, total_expense, session['user_id'])
            )
            conn.commit()
            conn.close()

            flash('Receipt uploaded and processed successfully!', 'success')
            return redirect(url_for('view_receipts'))
        else:
            flash('Invalid file format. Please upload a valid image.', 'error')
    return render_template('index.html')

# Function to process the uploaded receipt image and extract categorized text
def process_receipt_image(filepath):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

    # Extract items, quantities, and prices (simple placeholder logic)
    lines = extracted_text.split('\n')
    total_expense = 0
    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and parts[-1].replace('.', '', 1).isdigit():
            total_expense += float(parts[-1])
    return extracted_text, total_expense

# Route to view all receipts
@app.route('/view_receipts')
def view_receipts():
    if 'user_id' not in session:
        flash('Please log in to view receipts.', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    receipts = conn.execute('SELECT * FROM receipts WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('view_receipts.html', receipts=receipts)

# Placeholder routes
@app.route('/visualize')
def visualize():
    flash('Visualization feature coming soon!', 'info')
    return redirect(url_for('upload_receipt'))

@app.route('/settings')
def settings():
    flash('Settings feature coming soon!', 'info')
    return redirect(url_for('upload_receipt'))

# Test Route
@app.route('/test')
def test():
    return '<h1>Test Page</h1>'

if __name__ == '__main__':
    app.run(debug=True)
