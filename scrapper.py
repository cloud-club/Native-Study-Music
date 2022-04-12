import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def get_music_data(data):
    json_list = list()

    for i in data.index:
        json_template = {
            "musicId": data['Rank'][i],
            "musicName": data['Title'][i],
            "singer": data['Singer'][i],
            "PlayTotal": 128,
            "musicFile": 'music_file_example',
        }
        json_data = str(json_template)
        json_list.append(json_data.replace("'", '"').replace('"[', '[').replace(']"', "]"))

    return json_list


def run():
    driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
    URL = 'https://www.melon.com/chart/index.htm'
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get the target information within 24hour (song, singer)
    songs = soup.select('div.ellipsis.rank01')
    singers = soup.select('div.ellipsis.rank02 > span.checkEllipsis')

    # Make a DataFrame
    list_song = [song.text.strip('\n') for song in songs]
    list_singer = [singer.text for singer in singers]
    data = pd.DataFrame(data=zip(range(1, 101), list_song, list_singer), columns=['Rank', 'Title', 'Singer'])

    # Close webdriver
    driver.close()
    driver.quit()

    music_data = get_music_data(data)

    return music_data
