import requests
import re
import json
from bs4 import BeautifulSoup
from values import baseurl_serie
from urllib.parse import parse_qs, urlparse

base_url = baseurl_serie

def get_streamingcommunity_json_page_data(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        app_element = soup.find('div', {'id': 'app'})
        if app_element:
            data_page_value = app_element.get('data-page')
            data_page_json = data_page_value.replace('&quot;', '"')
            serie_data = json.loads(data_page_json)
            return serie_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def get_streamingcommunity_search(subpath):

    full_url = base_url + subpath

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(full_url)
    series_data = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the element with id 'app' and extract the 'data-page' attribute
        app_element = soup.find('div', {'id': 'app'})
        if app_element:
            data_page_value = app_element.get('data-page')
            data_page_json = data_page_value.replace('&quot;', '"')
            # If you want to convert it to a Python dictionary, you can use json.loads
            serie_data = json.loads(data_page_json)
            titles = serie_data['props']['titles']

            for title in titles:
                name = title['name']
                url = base_url + "titles/" + str(title['id']) + "-" + str(title['slug'])
                trimmed_url = baseurl_serie[8:]
                image_url = "https://cdn." + trimmed_url + "images/" + title['images'][0]['filename']
                plot = title['name']
                single_data = {
                    "title": name,
                    "url": url,
                    "poster": image_url,
                    "plot": plot,
                    "year": 2023  # You can change the year value as needed
                }
                series_data.append(single_data)

        return series_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def get_streamingcommunity_episodes(path):
    episode_data = []
    serie_data = get_streamingcommunity_json_page_data(path)

    title = serie_data['props']['title']
    serie_id = str(title['id'])
     
    if title['seasons_count'] > 0:
        season_numbers = []
        for season in title['seasons']:
            season_numbers.append(season['number'])
        for n in season_numbers:
            url = path + "/stagione-" + str(n)
            season_data = get_streamingcommunity_json_page_data(url)
            loaded_season = season_data['props']['loadedSeason']
            for episode in loaded_season['episodes']:
                single_data = {
                        "title": str(n) + "x" + str(episode['number']) + ": " + episode['name'],
                        "url": base_url + "iframe/" + serie_id + "?episode_id=" + str(episode['id']),
                        "episode_number": episode['number'],
                    }
                episode_data.append(single_data)
    else:
        single_data = {
                "title": title['name'],
                "url": base_url + "iframe/" + serie_id,
                "episode_number": 0,
            }
        episode_data.append(single_data)

    return episode_data

def get_actual_serie_url(episode_url):
    response = requests.get(episode_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the iframe tag
        iframe_tag = soup.find('iframe')
        
        if iframe_tag:
            # Extract the video URL from the src attribute
            iframe_src = iframe_tag.get('src')
            response = requests.get(iframe_src)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                first_script = soup.body.find('script')
                script_content = first_script.text
        
                video_id = re.search(r'"id":(\d+)', script_content).group(1)
                token = re.search(r"'token': '([^']+)'", script_content).group(1)
                token480p = re.search(r"'token480p': '([^']+)'", script_content).group(1)
                token720p = re.search(r"'token720p': '([^']+)'", script_content).group(1)
                expires = re.search(r"'expires': '([^']+)'", script_content).group(1)

                
                # Creating the video URL
                video_url = f'https://vixcloud.co/playlist/{video_id}?token={token}&token480p={token480p}&token720p={token720p}&expires={expires}'
                return video_url

    return None

#print(get_streamingcommunity_episodes('https://streamingcommunity.claims/serietv/manifest/'))
#print(get_actual_serie_url('https://uprot.net/msfi/amFBWE9TSDNIRENWMzQxY3Uya3ZyQT09'))
#print(get_actual_serie_url('https://stayonline.pro/l/mVl88/'))
#print(get_streamingcommunity_search('search?q=manifest'))
#print(get_streamingcommunity_episodes('https://streamingcommunity.cz/titles/6881-tre-manifesti-a-ebbing-missouri/'))
#print(get_streamingcommunity_episodes('https://streamingcommunity.cz/titles/3069-ragazze-audaci'))
#print(get_actual_serie_url('https://streamingcommunity.cz/iframe/1533?episode_id=14189'))
