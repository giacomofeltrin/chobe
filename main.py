import os
import sys
from urllib.parse import urlencode, parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

from animeita import get_animesaturn

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')

VIDEOS = [
    {
        'genre': 'AnimeITA',
        'icon': None,
        'fanart': None,
        'movies': get_animesaturn()
    },
    {
        'genre': 'Horror',
        'icon': os.path.join(ICONS_DIR, 'Horror.png'),
        'fanart': os.path.join(FANART_DIR, 'Horror.jpg'),
        'movies': [
            {
                'title': 'House on Haunted Hill',
                'url': 'https://ia800203.us.archive.org/18/items/house_on_haunted_hill_ipod/house_on_haunted_hill_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=House_on_Haunted_Hill.jpg',
                'plot': 'Eccentric millionaire Frederick Loren (Vincent Price) invites five people to a "party" '
                        'he is throwing for his fourth wife, Annabelle (Carol Ohmart), '
                        'in an allegedly haunted house he has rented, promising to give them each $10,000 '
                        'with the stipulation that they must stay the entire night in the house after '
                        'the doors are locked at midnight.',
                'year': 1959,
            },
            {
                'title': 'Carnival of Souls',
                'url': 'https://ia600301.us.archive.org/8/items/CarnivalofSouls/CarnivalOfSouls_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Carnival_of_Souls_%25281962_pressbook_cover%2529.jpg',
                'plot': 'Carnival of Souls is a 1962 Independent film horror film starring Candace Hilligoss. Produced and directed by Herk Harvey '
                        'for an estimated $33,000, the film did not gain widespread attention when originally released, '
                        'as a B-movie; today, however, it is a cult classic.',
                'year': 1962,
            },
            {
                'title': 'The Screaming Skull',
                'url': 'https://ia801603.us.archive.org/10/items/TheScreamingSkull/TheScreamingSkull.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Poster_for_The_Screaming_Skull.jpg',
                'plot': 'A widower remarries and the couple move into the house he shared with his previous wife. '
                        'Only the ghost of the last wife might still be hanging around.',
                'year': 1958,
            },
        ],
    },
    {
        'genre': 'Comedy',
        'icon': os.path.join(ICONS_DIR, 'Comedy.png'),
        'fanart': os.path.join(FANART_DIR, 'Comedy.jpg'),
        'movies': [
            {
                'title': 'Charlie Chaplin\'s "The Vagabond"',
                'url': 'https://ia904601.us.archive.org/16/items/CC_1916_07_10_TheVagabond/CC_1916_07_10_TheVagabond.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=The_Vagabond_%25281916%2529.jpg',
                'plot': 'Charlie Chaplins 53rd Film Released July 10 1916 The Vagabond was a silent '
                        'film by Charlie Chaplin and his third film with Mutual Films. Released in 1916, '
                        'it co-starred Edna Purviance, Eric Campbell, Leo White and Lloyd Bacon. '
                        'This film echoed Chaplin\'s work on The Tramp, with more drama mixed in with comedy.',
                'year': 1916,
            },
            {
                'title': 'Sing A Song of Six Pants',
                'url': 'https://ia601508.us.archive.org/26/items/sing_a_song_of_six_pants/sing_a_song_of_six_pants_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=SingSong6PantsOneSheet47.JPG',
                'plot': 'The Three Stooges (Moe, Larry, Shemp) are tailors and are heavily in debt. '
                        'Could a big reward for the capture of a fugitive bank robber answer their financial prayers?',
                'year': 1947,
            },
            {
                'title': 'Steamboat Bill, Jr.',
                'url': 'https://ia904501.us.archive.org/32/items/SteamboatBillJr/Steamboat_Bill.Jr_512kb.mp4',
                'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Steamboat_bill_poster.jpg',
                'plot': 'Steamboat Bill, Jr. is the story of a naive, college-educated dandy who must prove himself '
                        'to his working-class father, a hot-headed riverboat captain, while courting the daughter of '
                        'his father\'s rival, who threatens to put Steamboat Bill, Sr. '
                        'and his paddle-wheeler out of business.',
                'year': 1928,
            },
        ],
    },
]


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(URL, urlencode(kwargs))


def get_genres():
    """
    Get the list of video genres

    Here you can insert some code that retrieves
    the list of video sections (in this case movie genres) from some site or API.

    :return: The list of video genres
    :rtype: list
    """
    return VIDEOS


def get_videos(genre_index):
    """
    Get the list of videofiles/streams.

    Here you can insert some code that retrieves
    the list of video streams in the given section from some site or API.

    :param genre_index: genre index
    :type genre_index: int
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[genre_index]


def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, 'Public Domain Movies')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get movie genres
    genres = get_genres()
    # Iterate through genres
    for index, genre_info in enumerate(genres):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info['genre'])
        # Set images for the list item.
        list_item.setArt({'icon': genre_info['icon'], 'fanart': genre_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre_info['genre'])
        info_tag.setGenres([genre_info['genre']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://chobe/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def list_videos(genre_index):
    """
    Create the list of playable videos in the Kodi interface.

    :param genre_index: the index of genre in the list of movie genres
    :type genre_index: int
    """
    genre_info = get_videos(genre_index)
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, genre_info['genre'])
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get the list of videos in the category.
    videos = genre_info['movies']
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use only poster for simplicity's sake.
        # In a real-life plugin you may need to set multiple image types.
        list_item.setArt({'poster': video['poster']})
        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setTitle(video['title'])
        info_tag.setGenres([genre_info['genre']])
        info_tag.setPlot(video['plot'])
        info_tag.setYear(video['year'])
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://chobe/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        url = get_url(action='play', video=video['url'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    # offscreen=True means that the list item is not meant for displaying,
    # only to pass info to the Kodi player
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

ABUTTONS = ["Recently Added", "Search"]

def get_abuttons():
    return ABUTTONS

def list_animeita():
    abuttons = get_abuttons()
    # Iterate through categories
    for abutton in abuttons:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=abutton)
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': abutton, 'genre': abutton})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='abutton', abutton=abutton)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

CATEGORIES = [
    {
        'category': 'AnimeITA',
        'icon': None,
        'fanart': None,
        'main_menu': 'list_animeita'
    },
    {
        'category': 'Serie',
        'icon': None,
        'fanart': None,
        'main_menu': 'list_serie'
    }
]

def get_categories():
    return CATEGORIES

def list_categories():
    categories = get_categories()
    for index, category_info in enumerate(categories):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=category_info['category'])
        # Set images for the list item.
        list_item.setArt({'icon': category_info['icon'], 'fanart': category_info['fanart']})
        # Create a URL for a plugin recursive call.
        url = get_url(action='opencategory', category_menu=category_info['main_menu'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if not params:
        list_categories()
    elif params['action'] == 'opencategory':
        if params['category_menu'] == 'list_animeita':
            list_animeita()
        else: 
            list_animeita()
    if params['action'] == 'abutton':
        list_avideos(params['abutton'])
    elif params['action'] == 'listing':
        list_videos(int(params['genre_index']))
    elif params['action'] == 'play':
        play_video(params['video'])
    else:
        raise ValueError(f'Invalid paramstring: {paramstring}!')

if __name__ == '__main__':
    router(sys.argv[2][1:])