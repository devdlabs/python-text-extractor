from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import os

# Register Times New Roman font - ubuntu linux font path
try:
    pdfmetrics.registerFont(TTFont('TimesNewRoman', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'))
except Exception as e:
    print(f"Error registering font: {e}")

# Function to convert extracted text to PDF
def image_to_pdf(input_image_path, output_pdf_path, font_name="TimesNewRoman", font_size=12):
    # Load the image
    try:
        img = Image.open(input_image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Extract text from the image using Tesseract
    extracted_text = pytesseract.image_to_string(img)

    # Create a new PDF using ReportLab
    can = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4  # A4 dimensions

    # Set font to Times New Roman and font size
    can.setFont(font_name, font_size)

    # Margin setup for better formatting
    margin_x = 50
    margin_y = 50
    current_y = height - margin_y  # Start from the top of the page

    # Split the text into lines to fit the page
    lines = extracted_text.split('\n')
    
    for line in lines:
        # If there's not enough space on the current page, add a new page
        if current_y < margin_y:
            can.showPage()  # Create a new page
            can.setFont(font_name, font_size)  # Reset font for the new page
            current_y = height - margin_y
        
        # Draw the current line
        can.drawString(margin_x, current_y, line)
        current_y -= font_size + 5  # Move down by the font size + small spacing

    # Save the PDF
    can.save()

# Function to process images from src directory
def extract_text_from_image_to_pdf(src_dir="image-files", dest_dir="pdf-files", font_name="TimesNewRoman", font_size=12):
    try:
        # Get a sorted list of PDF filenames
        lines = sorted(os.listdir(src_dir))
        
        # Ensure output directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Process each image listed in the text file
        for line in lines:
            image_path = line.strip()  # Remove leading/trailing whitespace/newlines
            if image_path:  # Ensure it's not an empty line
                # Add directory path to image
                imagewithpath = f"{src_dir}/{image_path}"
                
                # Extract filename without extension for the PDF name
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_pdf_path = f"{dest_dir}/{base_name}.pdf"
                
                print(f"Processing: {image_path} {imagewithpath} -> {output_pdf_path}")
                
                # Convert the image to PDF
                image_to_pdf(imagewithpath, output_pdf_path, font_name, font_size)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

#extract text from Image to PDF 
extract_text_from_image_to_pdf("image-files", "pdf-files", "TimesNewRoman", 12)