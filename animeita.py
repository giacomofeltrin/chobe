import requests
import json
from bs4 import BeautifulSoup

def get_animesaturn_filter(subpath):
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

        return anime_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
def get_animesaturn_search(subpath):
    # Define the URL to scrape
    base_url = 'https://www.animesaturn.tv/'
    full_url = base_url + subpath


    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(full_url)
    anime_data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_contfilterent = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_contfilterent, 'html.parser')

        # Find and extract the desired information (as shown in the previous code)
        anime_list = soup.find_all('li', class_='list-group-item bg-dark-as-box-shadow')

        for item in anime_list:
            title_link = item.find('a', class_='badge badge-archivio badge-light')
            title = title_link.get_text(strip=True)
            url = title_link['href']
            image_url = item.find('img', class_='rounded copertina-archivio')['src']
            plot = item.find('p', class_='trama-anime-archivio text-white rounded').get_text(strip=True)

            # Create a dictionary to store the extracted data
            single_data = {
                "title": title,
                "url": url,
                "poster": image_url,
                "plot": plot,
                "year": 2023  # You can change the year value as needed
            }

            anime_data.append(single_data)

        return anime_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def get_animesaturn_episodes(path):

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(path)
    episode_data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and extract the desired information
        episodes_buttons = soup.find_all('a', class_='btn btn-dark mb-1 bottone-ep')

        for button in episodes_buttons:
            temp_url = button['href']
            title = button.get_text(strip=True)

            # Extract the episode number from the title
            episode_number = title.strip("Episodio ")

            # Get the actual url
            second_response = requests.get(temp_url)
            second_html_content = second_response.text
            second_soup = BeautifulSoup(second_html_content, 'html.parser')
            watch_link = second_soup.find('a', href=lambda href: href and "watch?file" in href)
            watch_url = watch_link['href']

            third_response = requests.get(watch_url)
            third_html_content = third_response.text
            third_soup = BeautifulSoup(third_html_content, 'html.parser')
            video_source = third_soup.find('source', type='video/mp4')
            mp4_url = video_source['src']


            # Create a dictionary to store the extracted data
            single_data = {
                "title": title,
                "url": mp4_url,
                "episode_number": episode_number,
            }

            episode_data.append(single_data)

        return episode_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

#print(get_animesaturn_episodes('https://www.animesaturn.tv/anime/Dorohedoro-aaaaa'))