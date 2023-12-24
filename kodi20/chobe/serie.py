import requests
import re
import json
from bs4 import BeautifulSoup
from values import baseurl_serie

base_url = baseurl_serie

def get_cb01_search(subpath):

    full_url = base_url + subpath

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(full_url)
    anime_data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')


        # Find and extract the desired information
        card_contents = soup.find_all('div', class_='card-content')

        for card_content in card_contents:
            title_link = card_content.find('a', href=True)
            if title_link:
                title = title_link.get_text(strip=True)
                url = title_link['href']
                
                # Check if the img tag exists before accessing the src attribute
                image_tag = card_content.find('img', src=True)
                image_url = image_tag['src'] if image_tag else None
                
                plot = card_content.find('p').get_text(strip=True)

                # Create a dictionary to store the extracted data
                single_data = {
                    "title": title,
                    "url": url,
                    "poster": image_url,
                    "plot": plot,
                    "year": 2023  # You can change the year value as needed
                }

                anime_data.append(single_data)
            else:
                print(f"No title link found in card-content div.")

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
            episode_url = button['href']
            title = button.get_text(strip=True)

            # Extract the episode number from the title
            episode_number = title.strip("Episodio ")

            # Create a dictionary to store the extracted data
            single_data = {
                "title": title,
                "url": episode_url,
                "episode_number": episode_number,
            }

            episode_data.append(single_data)

        return episode_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def scrape_m3u8_url(watch_url):
    response = requests.get(watch_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all script tags
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        # Extract the content of the script tag
        script_content = script_tag.string

        if script_content:
            # Check if "jwplayer" is present in the script content
            if 'jwplayer' in script_content:
                # Use regular expression to find the M3U8 URL
                m3u8_url_match = re.search(r'file:\s*"(https://[^"]+\.m3u8)"', script_content)
                
                if m3u8_url_match:
                    m3u8_url = m3u8_url_match.group(1)
                    return m3u8_url

    return None


def get_actual_anime_url(episode_url):
    second_response = requests.get(episode_url)
    second_html_content = second_response.text
    second_soup = BeautifulSoup(second_html_content, 'html.parser')
    watch_link = second_soup.find('a', href=lambda href: href and "watch?file" in href)
    watch_url = watch_link['href']
    third_response = requests.get(watch_url)
    third_html_content = third_response.text
    third_soup = BeautifulSoup(third_html_content, 'html.parser')
    video_source = third_soup.find('source', type='video/mp4')
    
    if video_source:
        video_url = video_source['src']
    else:
        # If 'video_source' is None, try scraping the M3U8 URL
        video_url = scrape_m3u8_url(watch_url)
    return(video_url)

#print(get_actual_anime_url('https://www.animesaturn.tv/ep/Boku-no-Hero-Academia-5-ITA-ep-5'))
#print(get_actual_anime_url('https://www.animesaturn.tv/ep/Frieren-Beyond-Journeys-End-ep-1'))
#print(get_animesaturn_episodes('https://www.animesaturn.tv/anime/Dorohedoro-aaaaa'))
print(get_cb01_search('serietv/?s=natale'))