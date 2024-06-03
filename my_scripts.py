import platform
from tempfile import TemporaryDirectory
from pathlib import Path
import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Set Tesseract path for Windows (update with your actual path)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your PDF file
PDF_file = Path(r"D:\my_project_folder\pdf_files\d.pdf")

def extract_info(text):
    """Extracts relevant information from the text."""
    # Regular expressions for extracting phone numbers and email addresses
    phone_pattern = re.compile(r"\b\d{10}\b")
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    # Initialize variables to store extracted info
    first_name = ""
    last_name = ""
    phone_numbers = []
    email_addresses = []
    lines_starting_with_hash = []

    # Split the text into lines
    lines = text.splitlines()

    for line in lines:
        # Extract first name
        if line.startswith("First Name:"):
            first_name = line.replace("First Name:", "").strip()

        # Extract last name
        elif line.startswith("Last Name:"):
            last_name = line.replace("Last Name:", "").strip()

        # Extract phone numbers
        phone_matches = phone_pattern.findall(line)
        phone_numbers.extend(phone_matches)

        # Extract email addresses
        email_matches = email_pattern.findall(line)
        email_addresses.extend(email_matches)

        # Extract lines starting with '#'
        if line.startswith("#"):
            lines_starting_with_hash.append(line)

    return first_name, last_name, phone_numbers, email_addresses, lines_starting_with_hash

def main():
    with TemporaryDirectory() as tempdir:
        pdf_pages = convert_from_path(PDF_file, 500)  # No need for Poppler path

        image_file_list = []
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}/page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        # Initialize output file
        text_file = Path("out_text.txt")

        with open(text_file, "a") as output_file:
            for image_file in image_file_list:
                # Extract text using Tesseract
                text = pytesseract.image_to_string(Image.open(image_file))
                text = text.replace("-\n", "")

                # Extract relevant information
                first_name, last_name, phone_numbers, email_addresses, lines_with_hash = extract_info(text)

                # Write extracted info to the output file
                output_file.write(f"First Name: {first_name}\n")
                output_file.write(f"Last Name: {last_name}\n")
                output_file.write(f"Phone Numbers: {', '.join(phone_numbers)}\n")
                output_file.write(f"Email Addresses: {', '.join(email_addresses)}\n")
                output_file.write(f"Lines starting with '#':\n")
                for line in lines_with_hash:
                    output_file.write(f"{line}\n")

if __name__ == "__main__":
    main()
