from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

def preprocess_image(filepath):
    """
    Preprocess the image to improve OCR accuracy.
    """
    image = Image.open(filepath)
    # Convert image to grayscale
    image = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # Apply binarization
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    return image

def extract_text(filepath):
    """
    Extract text from an image using Tesseract OCR with preprocessing.
    """
    try:
        preprocessed_image = preprocess_image(filepath)
        # Custom Tesseract configuration for better accuracy
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
        return text
    except Exception as e:
        return f"Error during OCR: {e}"

if __name__ == "__main__":
    # Example usage
    input_image = "path_to_your_image.jpeg"  # Replace with your image path
    extracted_text = extract_text(input_image)
    print("Extracted Text:")
    print(extracted_text)
