import requests
import json
from bs4 import BeautifulSoup

def get_animesaturn(subpath):
    # Define the URL to scrape
    base_url = 'https://www.animesaturn.tv/'
    full_url = base_url + subpath

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(full_url)
    anime_data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and extract the desired information (as shown in the previous code)
        anime_cards = soup.find_all(class_='anime-card-newanime')

        for card in anime_cards:
            # Extract anime title and URL
            title = card.find('a', title=True).get('title')
            url = card.find('a', href=True).get('href')
            image_url = card.find('img', class_='new-anime').get('src')

            # Example data structure for a single movie
            single_data = {
                "title": title,
                "url": url,
                "poster": image_url,
                "plot": '',
                "year": 2023
            }

            anime_data.append(single_data)

        print(anime_data)
        return anime_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None