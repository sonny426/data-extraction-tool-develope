import streamlit as st
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

def main():
    st.title("PDF Upload and Save")

    # File uploader allows only PDF files
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file to local storage
        file_path = save_uploaded_file(uploaded_file)

        if file_path:
            st.success(f"File saved successfully: {file_path}")
        else:
            st.error("Failed to save file")

if __name__ == "__main__":
    main()
