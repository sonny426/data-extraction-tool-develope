import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os

def save_uploaded_file(uploaded_file):
    try:
        # Create a directory to store the uploaded file
        os.makedirs('uploaded_pdfs', exist_ok=True)

        # Define the file path
        file_path = os.path.join('uploaded_pdfs', uploaded_file.name)

        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path
    except Exception as e:
        return None

def pdf_to_images(pdf_path):
    images = []
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Iterate over each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Get the pixmap (image) of the page
            pix = page.get_pixmap()

            # Create an image from the pixmap
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

            # Save the image to a directory
            os.makedirs('pdf_images', exist_ok=True)
            img.save(os.path.join('pdf_images', f'page_{page_num + 1}.png'))

        return images
    except Exception as e:
        st.error(f"Failed to convert PDF to images: {e}")
        return []

def main():
    st.title("PDF Upload and Save")

    # File uploader allows only PDF files
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file to local storage
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"File saved successfully: {file_path}")
            # Convert PDF to images
            images = pdf_to_images(file_path)

            # Display the images in the Streamlit app
            st.image(images, caption=[f'Page {i+1}' for i in range(len(images))], use_column_width=True)
        else:
            st.error("Failed to save file")

if __name__ == "__main__":
    main()
