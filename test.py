import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

base_url = 'https://rayon.in.ua/news'
max_page = 5705 
page_number = 1 
wait_time = 5 

csv_file = open('news.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['title', 'description', 'date', 'url'])

while page_number <= max_page:
    url = f'{base_url}?page={page_number}'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    titles = soup.find_all(class_='item-newslist__title')
    descriptions = soup.find_all(class_='item-newslist__text')
    dates = soup.find_all(class_='item-newslist__date')
    links = soup.find_all(class_='item-newslist__link')
    
    for title, description, date, link in zip(titles, descriptions, dates, links):
        writer.writerow([title.get_text(strip=True), 
                         description.get_text(strip=True), 
                         date.get_text(strip=True), 
                         link['href']])
    
    print(f'Scraped page {page_number}')
    
    page_number += 1
    
    # Wait before flipping to the next page
    time.sleep(wait_time)

csv_file.close()
print(f'Scraping completed up to page {max_page}')
