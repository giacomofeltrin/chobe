import requests
import re
import json
from bs4 import BeautifulSoup
from values import baseurl_serie

base_url = baseurl_serie

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
                url = base_url + "titles/" + str(title['id'])
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
                        # Return the link immediatly if "stayonline" otherwise explore subfolder
                        if "stayonline" in l:
                            single_data = {
                                    "title": episode_text + l,
                                    "url": l,
                                    "season_number": current_season,
                                }
                            episode_data.append(single_data)
                        else:
                            response_internal = requests.get(l)
                            if response_internal.status_code == 200:
                                html_content = response_internal.text
                                soup = BeautifulSoup(html_content, 'html.parser')
                                for row in soup.find_all('tr'):
                                    columns = row.find_all('td')
                                    if len(columns) >= 3:
                                        episode_text = columns[0].text.strip()
                                        link = columns[1].find('a')['href']
                                        single_data = {
                                            "title": episode_text,
                                            "url": link,
                                            "season_number": current_season,
                                        }
                                        episode_data.append(single_data)
        return episode_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def get_actual_serie_url(episode_url):
    video_url = episode_url
    if "uprot" in episode_url:
        uprot_response = requests.get(episode_url)
        if uprot_response.status_code == 200:
            html_content = uprot_response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            video_link_tag = soup.find('a', href=True)
            video_url = video_link_tag['href'] if video_link_tag else None


    '''
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
    '''
    return(video_url)

#print(get_streamingcommunity_episodes('https://streamingcommunity.claims/serietv/manifest/'))
#print(get_actual_serie_url('https://uprot.net/msfi/amFBWE9TSDNIRENWMzQxY3Uya3ZyQT09'))
#print(get_actual_serie_url('https://stayonline.pro/l/mVl88/'))
print(get_streamingcommunity_search('search?q=manifest'))