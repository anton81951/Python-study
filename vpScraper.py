import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime, timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Date range
start_date = datetime.strptime('03-03-2023', '%d-%m-%Y')
end_date = datetime.strptime('31-07-2024', '%d-%m-%Y')
date_format = '%d-%m-%Y'

# Open CSV file for writing
with open('news_volynpost_archive.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Title', 'Description', 'Date', 'URL'])

    current_date = end_date
    while current_date >= start_date:
        url = f'https://www.volynpost.com/archive/{current_date.strftime(date_format)}'
        print(f'Scraping URL: {url}')
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract news items
            news_items = soup.find_all('div', class_='item')

            for item in news_items:
                # Extract the URL, title, description, and date for each news item
                link_tag = item.find('a', href=True)
                if not link_tag:
                    continue  # Skip if no link is found
                
                news_url = link_tag['href']

                # Find the content div
                content_div = item.find('div', class_='content')
                if not content_div:
                    continue  # Skip if content div is not found

                # Extract title from the link tag inside content div
                title_tag = content_div.find('a', href=True)
                title = title_tag.get_text(strip=True) if title_tag else 'No title found'

                # Extract date
                date_div = content_div.find('div', class_='date')
                date_text = date_div.get_text(strip=True) if date_div else 'No date found'

                # Extract description
                description_div = content_div.find_all('div')[1]  # Get the second div inside content
                description = description_div.get_text(strip=True) if description_div else 'No description found'

                writer.writerow([
                    title,
                    description,
                    date_text,
                    news_url
                ])

            print(f'Scraped {url}')

        except requests.RequestException as e:
            print(f'Error fetching {url}: {e}')
        except Exception as e:
            print(f'Error parsing {url}: {e}')

        # Move to the previous date
        current_date -= timedelta(days=1)
        time.sleep(1)  # Adjust the sleep time as needed

print('Scraping completed.')
