import requests
import json
from bs4 import BeautifulSoup

def get_animesaturn():
    # Define the URL to scrape
    url = 'https://www.animesaturn.tv/filter'

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and extract the desired information (as shown in the previous code)

        anime_data = []

        anime_genres = soup.find_all('div', class_='genres-rows')

        for genre_row in anime_genres:
            genre_name = genre_row.find('h2').text.strip()

            movies = []
            movie_cards = genre_row.find_all('div', class_='anime-card-newanime main-anime-card')

            for card in movie_cards:
                # Extract anime title and URL
                title = card.find('a', title=True).get('title')
                url = card.find('a', href=True).get('href')
                image_url = card.find('img', class_='new-anime').get('src')

                # Example data structure for a single movie
                movie_data = {
                    "title": title,
                    "url": url,
                    "poster": image_url,
                    "plot": '',  # You can add plot information if available
                    "year": None  # You can add the year if available
                }

                movies.append(movie_data)

            genre_data = {
                'genre': genre_name,
                'icon': '',  # You can set the icon path if needed
                'fanart': '',  # You can set the fanart path if needed
                'movies': movies
            }

            anime_data.append(genre_data)

        return anime_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

anime_data = get_animesaturn()
VIDEOS = anime_data

print(anime_data)
