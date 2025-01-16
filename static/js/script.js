document.addEventListener('DOMContentLoaded', () => {
    // Confirmation for deleting a receipt
    const deleteLinks = document.querySelectorAll('a.text-red-500');
    deleteLinks.forEach(link => {
        link.addEventListener('click', async event => {
            event.preventDefault();
            const confirmDelete = confirm('Are you sure you want to delete this receipt? This action cannot be undone.');
            if (confirmDelete) {
                try {
                    const response = await fetch(link.getAttribute('href'), { method: 'POST' });
                    if (response.ok) {
                        alert('Receipt deleted successfully!');
                        link.closest('tr').remove(); // Remove the row from the table (if applicable)
                    } else {
                        alert('Failed to delete receipt.');
                    }
                } catch (error) {
                    alert('Error occurred while deleting receipt.');
                }
            }
        });
    });

    // Add click event listener for "View" links
    const viewLinks = document.querySelectorAll('a.text-blue-500');
    viewLinks.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            // Navigate to the view receipt details page
            const receiptUrl = link.getAttribute('href');
            window.location.href = receiptUrl;
        });
    });

    // Handle file upload and display receipt image with highlights
    const uploadInput = document.getElementById('uploadInput');
    if (uploadInput) {
        uploadInput.addEventListener('change', handleFileUpload);
    }

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            // Validate file size (limit to 5MB) and type
            if (file.size > 5 * 1024 * 1024) {
                alert('File size must be less than 5MB.');
                event.target.value = '';
                return;
            }
            const validTypes = ['image/png', 'image/jpeg', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                alert('Invalid file type. Please upload an image file.');
                event.target.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                const image = document.getElementById('receiptImage');
                image.src = e.target.result;

                // Clear previous highlights
                const canvas = document.getElementById('highlightCanvas');
                const context = canvas.getContext('2d');
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Set canvas size to match the image
                setTimeout(() => {
                    canvas.width = image.width;
                    canvas.height = image.height;
                    highlightScannedParts();
                }, 100);
            };
            reader.readAsDataURL(file);
        }
    }

    async function highlightScannedParts() {
        const canvas = document.getElementById('highlightCanvas');
        const context = canvas.getContext('2d');

        try {
            const response = await fetch('/api/scanned-parts'); // Replace with your actual API endpoint
            const scannedParts = await response.json();

            context.strokeStyle = 'red';
            context.lineWidth = 2;

            scannedParts.forEach(part => {
                context.strokeRect(part.x, part.y, part.width, part.height);
            });
        } catch (error) {
            console.error('Error fetching scanned parts:', error);
        }
    }

    // Function to display current date and time
    function displayDateTime() {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        };
        const formattedDate = now.toLocaleDateString('en-US', options) + ' ' + now.toLocaleTimeString('en-US', options);

        const dateTimeElement = document.getElementById('currentDateTime');
        if (dateTimeElement) {
            dateTimeElement.textContent = formattedDate;
        }
    }

    // Update date and time every second
    setInterval(displayDateTime, 1000);

    // Call the function when the page loads
    displayDateTime();

    // Drag-and-drop functionality for file upload
    const dropArea = document.getElementById('dropArea');
    if (dropArea) {
        dropArea.addEventListener('dragover', event => {
            event.preventDefault();
            dropArea.classList.add('drag-over');
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('drag-over');
        });

        dropArea.addEventListener('drop', event => {
            event.preventDefault();
            dropArea.classList.remove('drag-over');
            const file = event.dataTransfer.files[0];
            if (file) {
                uploadInput.files = event.dataTransfer.files; // Simulate input selection
                uploadInput.dispatchEvent(new Event('change'));
            }
        });
    }
});
