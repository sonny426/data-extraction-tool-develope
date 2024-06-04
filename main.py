import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
from openai import OpenAI
import base64
import instructor
import requests
from pydantic.main import BaseModel

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

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

class RecordDetail(BaseModel):
    TITLE: str
    STUDIO: str
    GENRE: str
    ARENA: str
    MODIFIED_ON: str
    SEASON: str
    STATUS: str

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

            for page in range(10):

                image_path = f"pdf_images/page_{page + 2}.png"
                base64_image = encode_image(image_path)

                client = instructor.patch(OpenAI())

                payload = {
                    "model": "gpt-4-vision-preview",
                    "messages": [
                    {
                        "role": "user",
                        "content": [
                        {
                            "type": "text",
                            "text": """
                                This image is a sample report. Please provide the data in JSON format shown below witout any description.
                                If there are multiple values for each field, seperate by ','.
                                {
                                    TITLE,
                                    STUDIO,
                                    GENRE,
                                    ARENA,
                                    MODIFIED_ON,
                                    SEASON,
                                    STATUS,
                                    NETWORK,
                                    TERRITORY,
                                    SCHEDULE,
                                    COCOMMISSION1,
                                    COTERRITORY1,
                                    COCOMMISSION2,
                                    COTERRITORY2,
                                    ...
                                }
                                The second row contains these values: TITLE, STUDIO, MODIFIED_ON.
                                GENRE is data only from table at position (2,3), don't need information from others.
                                ARENA is data only from table at position (2,4), don't need information from others.
                                And the bottom row of each record table contains information on the season number.
                                And the third row from the bottom of each record table contains information on the production status.
                                Starting in the third row from the top of each record there are rows with information on the networks for the TV series.
                                Networks are identified with logos. You should get NETWORK information from the logo.
                                And you can get TERRITORY, SCHEDULE from thrid row.
                                Many records will have additional rows with information about additional networks.  For example the first record contains three additional rows with network information. I would like to add additional fields as follows for these additional networks
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                        ]
                    }
                    ],
                    "max_tokens": 3000
                }

                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                response_json = response.json()
                content = response_json['choices'][0]['message']['content']

                st.text(content)

                # record_detail = client.chat.completions.create(
                #     model="gpt-4",
                #     response_model=RecordDetail,
                #     messages=[
                #         {"role": "user", "content": "Extract TITLE, STUDIO, GENRE, ARENA, MODIFIED_ON, SEASON, STATUS from the following record description json:" + content},
                #     ]
                # )

                # st.text(record_detail)

        else:
            st.error("Failed to save file")

if __name__ == "__main__":
    main()
