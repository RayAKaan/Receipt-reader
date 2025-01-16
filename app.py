import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from ocr_processor import extract_text  # Import the extract_text function from ocr-processor.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')  # Get secret key from environment

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize SQLite database
DATABASE = 'database/receipts.db'

def init_db():
    """Initialize the SQLite database and tables."""
    if not os.path.exists('database'):
        os.makedirs('database')
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                extracted_text TEXT,
                total_expense REAL,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Add 'category' column if it doesn't exist
        cursor.execute("PRAGMA table_info(receipts)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'category' not in columns:
            cursor.execute("ALTER TABLE receipts ADD COLUMN category TEXT")
        conn.commit()

# Initialize the database
init_db()

# Function to check allowed file extensions
def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home Route (Redirects to the upload page)
@app.route('/', methods=['GET'])
def home():
    """Redirect users directly to the upload page."""
    return redirect(url_for('upload_receipt'))  # Direct users to the upload_receipt page

# Route to upload receipt
@app.route('/upload', methods=['GET', 'POST'])
def upload_receipt():
    """Upload a receipt image."""
    if request.method == 'POST':
        if 'receipt' not in request.files:
            flash("No file part.", "error")
            return redirect(request.url)
        file = request.files['receipt']
        if file.filename == '':
            flash("No selected file.", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            extracted_text, total_expense, category = process_receipt_image(filepath)

            # Save receipt to the database
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    'INSERT INTO receipts (filename, extracted_text, total_expense, category) VALUES (?, ?, ?, ?)',
                    (filename, extracted_text, total_expense, category)
                )
                conn.commit()

            flash("Receipt uploaded successfully!", "success")
            return redirect(url_for('upload_receipt'))

    # Fetch overview data for graph
    overview_data = get_overview_data()
    return render_template('upload-receipt.html', overview_data=overview_data)

# Function to process the uploaded receipt image and extract categorized text
def process_receipt_image(filepath):
    """Extract text, total expense, and category from a receipt image."""
    print(f"Processing receipt: {filepath}")
    extracted_text = extract_text(filepath)  # Assume OCR logic is implemented
    total_expense = 100.50  # Dummy expense
    category = "Restaurant"  # Dummy category for now, modify based on receipt analysis
    return extracted_text, total_expense, category

# Function to fetch overview data for graph
def get_overview_data():
    """Fetch overview data for spending categories."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(total_expense) FROM receipts GROUP BY category')
        results = cursor.fetchall()
    
    # Ensure `results` is properly structured
    overview_data = {
        "labels": [row[0] if row[0] else "Unknown" for row in results],  # Handle possible `None` categories
        "data": [row[1] if row[1] else 0 for row in results],  # Ensure no `None` values
    }
    return overview_data

# Route to view detailed expense graphs
@app.route('/expense_graphs')
def expense_graphs():
    """Display detailed expense graphs."""
    overview_data = get_overview_data()
    return render_template('expense-graphs.html', overview_data=overview_data)

# Route to view all receipts
@app.route('/view_receipts')
def view_receipts():
    """View all receipts."""
    with sqlite3.connect(DATABASE) as conn:
        receipts = conn.execute('SELECT * FROM receipts').fetchall()

    return render_template('view-receipts-as-list.html', receipts=receipts)

# Route to view receipt details
@app.route('/view_receipt_details/<int:receipt_id>')
def view_receipt_details(receipt_id):
    """View details of a specific receipt."""
    with sqlite3.connect(DATABASE) as conn:
        receipt = conn.execute('SELECT * FROM receipts WHERE id = ?', (receipt_id,)).fetchone()

    if receipt:
        return render_template('view-receipt-details.html', receipt=receipt)
    else:
        flash("Receipt not found.", "error")
        return redirect(url_for('view_receipts'))

# Route to delete a receipt
@app.route('/delete_receipt/<int:receipt_id>', methods=['POST'])
def delete_receipt(receipt_id):
    """Delete a receipt from the database."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM receipts WHERE id = ?', (receipt_id,))
        conn.commit()

    flash("Receipt deleted successfully.", "success")
    return redirect(url_for('view_receipts'))

if __name__ == '__main__':
    app.run(debug=True)
