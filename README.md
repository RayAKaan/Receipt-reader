# Receipt Reader

**Receipt Reader** is a dynamic web application designed to help users manage their expenses effectively. The platform allows users to upload receipts, categorize expenses, and visualize spending trends using detailed graphs and charts. This project is powered by Python, Flask, and SQLite, with a sleek user interface built using Tailwind CSS.

---

## Features

1. **Receipt Upload**
   - Users can upload images of receipts in various formats (JPG, JPEG, PNG, PDF).
   - The application uses OCR (Optical Character Recognition) to extract text from uploaded receipts.

2. **Expense Categorization**
   - Extracted text is analyzed and categorized (e.g., Restaurants, Petrol, Shopping).
   - The total expense is calculated and stored in the database.

3. **Visualization**
   - A bar chart on the upload page provides an overview of expenses by category.
   - A dedicated detailed graph page displays expense breakdowns by days, weeks, months, or years.

4. **View Receipts**
   - Users can view a list of all uploaded receipts with timestamps.
   - Each receipt entry displays detailed extracted text, categorized expenses, and more.

5. **Delete Receipts**
   - Users can delete specific receipts from the database.

---

## Tech Stack

### Backend
- **Python**: The core programming language used for server-side logic.
- **Flask**: A lightweight web framework for building the application.
- **SQLite**: A lightweight relational database used to store receipts and extracted data.

### Frontend
- **HTML5**: For structuring the web pages.
- **CSS3 with Tailwind CSS**: For designing a responsive and modern user interface.
- **JavaScript**: For interactivity and integrating Chart.js.
- **Chart.js**: Used to generate interactive graphs and charts for expense visualization.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/RayAKaan/Receipt-reader.git
   cd Receipt-reader
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   The application uses SQLite. Ensure the `receipts.db` database file is initialized.
   ```bash
   python app.py  # This will create the database and required tables
   ```

5. **Run the Application**
   ```bash
   flask run
   ```
   The application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## How to Use

### Upload a Receipt
1. Navigate to the **Upload Receipt** page.
2. Click "Select Receipt File" to choose an image or PDF of your receipt.
3. Click the "Upload Receipt" button to process the receipt.

### View Expenses
- **Spending Overview**: View a bar chart showing expenses by category on the Upload Receipt page.
- **Detailed Graphs**: Click the chart to see detailed expense breakdowns by day, week, month, or year.

### Manage Receipts
- **View All Receipts**: Click the "View All Receipts" button to see a list of all uploaded receipts.
- **Delete Receipts**: Use the delete button next to a receipt to remove it from the database.

---

## File Structure

```
Receipt-reader/
├── app.py               # Main Flask application
├── database/            # Database folder
│   └── receipts.db      # SQLite database file
├── templates/           # HTML templates
│   ├── upload-receipt.html
│   ├── view-receipts-as-list.html
│   ├── view-receipt-details.html
│   └── expense-graphs.html
├── static/              # Static files
│   ├── css/             # Custom styles
│   └── js/              # JavaScript files
├── ocr_processor.py     # OCR text extraction logic
├── requirements.txt     # Python dependencies
└── README.md            # Documentation (this file)
```

---

## Future Improvements
- **User Authentication**: Add login and signup features for individual expense tracking.
- **Advanced Filtering**: Provide options to filter expenses by custom date ranges.
- **Cloud Integration**: Enable receipt storage and access via cloud platforms.
- **Export Options**: Allow users to download their expense data in CSV or Excel format.

---

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Open a pull request on the main repository.

---

## Contact
For any questions or feedback, please contact:
- **Rayyan Ahmed Khan**
- Email: rakrayyan16@gmail.com

