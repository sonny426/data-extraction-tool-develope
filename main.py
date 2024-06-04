import streamlit as st
import fitz  # PyMuPDF
import os
import requests
from bs4 import BeautifulSoup
import time
import random

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

def MyRequest(url):
    # Generate a random sleep duration between 2 to 3 seconds
    sleep_duration = random.uniform(1, 2)

    # Sleep for the generated duration
    time.sleep(sleep_duration)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "cook_autovisit=229fe602662a1f55c60e63af2c6d0aa4; _gcl_au=1.1.1518389169.1717424536; _mkto_trk=id:319-SAP-104&token:_mch-luminatedata.com-1717424536399-88663; _ga=GA1.1.2002600592.1717424538; addevent_track_cookie=35fcc815-71b7-49be-b842-4d6a69660ac9; cook_autologin=32e10156a031e64cc4c07d0c1a535751; _ga_3ESV50XWME=GS1.1.1717450761.1.1.1717451269.60.0.0; PHPSESSID=fcgbg4hfoobdgcn5vie57f3blc; home_page_tab=tab_dei; ci_session=VpjjbYZoEWGFXo7AEXLzld0FQ9UjY7y%2BcK19J3YsfQqWm5OSjZoAB%2BLmr%2F%2BIle3ijN3We1YTpu4wOZJrCt0XfrcO6zYziR1Fv8FZodv8xDmBBoKXOnt0dQqhyaYHTOKcZLuZGOuXRI9vUu0Y5rE5QSjEnH7gvGbL93JES%2B05NEv2tgL9XrAhaySUiwRQt1j3WvsLgBiCQthRRrrIJlOxJJm4Jwmwfv9U6xFz3x1y%2BfL%2Byv%2Bp9g9VwffsF4vDNFbAWx7JRp%2B0yGBFQvL%2FUnnUO%2BaNVS5GoOLsDGQAFZJBAoSrzvAXv%2F57gfe7K9UZfSUq%2BFHFrJvCZ4qaMgnmuurueP3%2BWk0eF80PNcrLiD%2FhswfWwaKUJ1jWc43Zfx2UDr0ld4U8j4h2MYlHy2QU4MAu%2B%2FP3aZZ3xVGNstBVAp1yG%2FM%3D; _dd_s=rum=1&id=f1b56134-19bf-42cf-bd2a-4473db8592e8&created=1717531035496&expire=1717531953976; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+04+2024+16%3A01%3A03+GMT-0400+(Eastern+Daylight+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0002%3A1%2CC0004%3A1%2CC0001%3A1%2CC0003%3A1; _ga_PDQYBV3900=GS1.1.1717529140.11.1.1717531264.0.0.0; AWSALB=eCQ8nuMUkrg4Sw/VCkg9fsenbCrBFiUWm6zVeWFWC++er+BLGcDoSDCK1OTnDzX3tmlN1mwc/as1k032rmaW1oPRGdcLmte+xVaaoIOfQkF3KRkI4+lHX7yssO0q; AWSALBCORS=eCQ8nuMUkrg4Sw/VCkg9fsenbCrBFiUWm6zVeWFWC++er+BLGcDoSDCK1OTnDzX3tmlN1mwc/as1k032rmaW1oPRGdcLmte+xVaaoIOfQkF3KRkI4+lHX7yssO0q",
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
    response = requests.get(url, headers=headers)

    return response

def main():
    st.title("PDF Upload and Save")

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
                response = MyRequest(link)
                soup = BeautifulSoup(response.content, 'html.parser')
                TITLE = soup.find('div', {'class': 'new-header-wrap-2'}).find('h1').text.strip()
                data = soup.find('table', {'class': 'p18table1'}).find('tbody').find('tr').find_all('td')
                STUDIO = ','.join([_.text.strip() for _ in data[0].find_all('a')])
                GENRE = ','.join([_.text.strip() for _ in data[1].find_all('a')])
                ARENA = ','.join([_.text.strip() for _ in data[2].find_all('a')])
                MODIFIED_ON = data[3].text.strip()
                SEASON = soup.find('div', {'class': 'prd-detailsleft'}).find(lambda tag: 'SEASON' in tag.get_text()).find('span').text.strip()
                STATUS = soup.find('div', {'class': 'prd-detailsleft'}).find(lambda tag: 'STATUS' in tag.get_text()).find('span').text.strip()
                data_cells = soup.find_all('div', {'class': 'p18rsec'})
                NETWORKS = []
                for data in data_cells:
                    data = data.find_all('p')
                    NETWORKS.append([data[0].find('a')['href'], data[1].text.strip(), data[-2].text.strip()])
                record = TITLE
                record += ' | ' + STUDIO
                record += ' | ' + GENRE
                record += ' | ' + ARENA
                record += ' | ' + MODIFIED_ON
                record += ' | ' + SEASON
                record += ' | ' + STATUS
                for index, NETWORK in enumerate(NETWORKS):
                    link = 'https://filmandtv.luminatedata.com/' + NETWORK[0]
                    response = MyRequest(link)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    COMPANY = soup.find('div', {'class': 'new-header-wrap-2'}).find('h1').text.strip()
                    record += ' | ' + COMPANY
                    record += ' | ' + NETWORK[1]
                    if index == 0:
                        record += ' | ' + NETWORK[2]
                count += 1
                st.success('Successfully scraped: ' + str(count) + '/' + str(len(links)))
                result = result + record + "\n"

            st.download_button(label="Download File", data=result, file_name='result.txt')

        else:
            st.error("Failed to save file")

if __name__ == "__main__":
    main()
