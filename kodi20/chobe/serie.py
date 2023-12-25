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
    serie_data = []

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

                serie_data.append(single_data)
            else:
                print(f"No title link found in card-content div.")

        return serie_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def get_cb01_episodes(path):
    response = requests.get(path)
    episode_data = []

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div containing all the season information
        season_divs = soup.find_all('div', class_='sp-wrap sp-wrap-default')

        current_season = "Unknown Season"

        # Iterate over each season
        for season_div in season_divs:
            current_season = season_div.find("div", class_="sp-head").text.strip()
            for episode in season_div.find_all("p"):
                episode_text = episode.text.strip()
                if episode_text:
                    links = [a["href"] for a in episode.find_all("a", href=True)]
                    for l in links:
                        
                        single_data = {
                                "title": episode_text + l,
                                "url": l,
                                "season_number": current_season,
                            }
                        print(single_data)
                        episode_data.append(single_data)
                        return episode_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
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
print(get_cb01_episodes('https://cb01.claims/serietv/manifest/'))