import streamlit as st
import fitz  # PyMuPDF
import os
import requests
from bs4 import BeautifulSoup
import time
import random
import json

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

def extract_links_from_pdf(pdf_path):
    # Open the PDF
    document = fitz.open(pdf_path)
    all_links = set()

    # Iterate over each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        links = page.get_links()
        for link in links:
            if 'uri' in link:
                if 'track_id' in link['uri']:
                    all_links.add(link['uri'])

    return all_links

def MyRequest(cookie, url):
    sleep_duration = random.uniform(0.5, 1)

    # Sleep for the generated duration
    time.sleep(sleep_duration)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": cookie,
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # Make the request
    response = requests.get(url, headers=headers).content
    return response

def main():
    st.title("PDF Upload and Save")

    cookie = st.text_input('Enter your cookie:')
    skip = st.number_input("Enter a number of skip record:", value=0)
    # File uploader allows only PDF files
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file to local storage
        pdf_path = save_uploaded_file(uploaded_file)

        if pdf_path:
            st.success(f"File saved successfully: {pdf_path}")
            links = extract_links_from_pdf(pdf_path)
            result = ""
            count = 0
            for link in links:
                if count < skip:
                    count += 1
                    continue
                response = MyRequest(cookie, link)
                SEASON = ''
                STATUS = ''
                STUDIO = ''
                GENRE = ''
                ARENA = ''
                MODIFIED_ON = ''
                soup = BeautifulSoup(response, 'html.parser')
                TITLE = soup.find('div', {'class': 'new-header-wrap-2'}).find('h1').text.strip()
                data = soup.find('table', {'class': 'p18table1'}).find('tbody').find('tr').find_all('td')
                try:
                    STUDIO = ','.join([_.text.strip() for _ in data[0].find_all('a')])
                    GENRE = ','.join([_.text.strip() for _ in data[1].find_all('a')])
                    ARENA = ','.join([_.text.strip() for _ in data[2].find_all('a')])
                    MODIFIED_ON = data[3].text.strip()
                except:
                    STUDIO = ''
                    GENRE = ''
                    ARENA = ''
                    MODIFIED_ON = ''
                try:
                    SEASON = soup.find('div', {'class': 'prd-detailsleft'}).find(lambda tag: 'SEASON' in tag.get_text()).find('span').text.strip()
                except:
                    SEASON = ''
                try:
                    STATUS = soup.find('div', {'class': 'prd-detailsleft'}).find(lambda tag: 'STATUS' in tag.get_text()).find('span').text.strip()
                except:
                    STATUS = ''
                data_cells = soup.find_all('div', {'class': 'p18rsec'})
                NETWORKS = []
                for data in data_cells:
                    data = data.find_all('p')
                    try:
                        NETWORKS.append([data[0].find('a')['href'], data[1].text.strip(), data[-2].text.strip()])
                    except:
                        continue
                record = TITLE
                record += ' | ' + STUDIO
                record += ' | ' + GENRE
                record += ' | ' + ARENA
                record += ' | ' + MODIFIED_ON
                record += ' | ' + SEASON
                record += ' | ' + STATUS
                for index, NETWORK in enumerate(NETWORKS):
                    try:
                        link = 'https://filmandtv.luminatedata.com/' + NETWORK[0]
                        response = MyRequest(cookie, link)
                        soup = BeautifulSoup(response, 'html.parser')
                        COMPANY = soup.find('div', {'class': 'new-header-wrap-2'}).find('h1').text.strip()
                        record += ' | ' + COMPANY
                        record += ' | ' + NETWORK[1]
                        if index == 0:
                            record += ' | ' + NETWORK[2]
                    except:
                        continue
                count += 1
                st.success('Successfully scraped: ' + str(count) + '/' + str(len(links)))
                result = result + record + "\n"

                st.download_button(label="Download File " + str(count), data=result, file_name='result.txt')

        else:
            st.error("Failed to save file")

if __name__ == "__main__":
    main()
