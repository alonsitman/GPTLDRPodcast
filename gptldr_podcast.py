from bs4 import BeautifulSoup
import re
import requests
from pydub import AudioSegment
from pathlib import Path
from transcriptor import get_transcript

import sys
import path
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
import GPTLDRCore.gptldr_core as gptldr_core

# Podcst URL
# https://podcasts.google.com/feed/aHR0cHM6Ly9sZXhmcmlkbWFuLmNvbS9mZWVkL3BvZGNhc3Qv/episode/aHR0cHM6Ly9sZXhmcmlkbWFuLmNvbS8_cD01NTk2?sa=X&ved=0CAUQkfYCahcKEwiorf3OjJuAAxUAAAAAHQAAAAAQAQ'
    

def podcast_title_mp3(url, mp3_filename):
    # Read the url and create soup object
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Get all the divs corresponding to each podcast episode
    divs = soup.find_all('div', attrs={'class': 'oD3fme'})

    # currently we're only interested in downloading the first podcast
    div = divs[0]

    # Iterate through each div (episode)
    # Get the date published
    date = div.find('div', attrs={'class': 'OTz6ee'}).text

    # Get the name of the episode and remove invalid characters (Windows)
    name = div.find('div', attrs={'class': 'e3ZUqe'}).text
    name = re.sub('[\/:*?"<>|]+', '', name)
    
    # Get the URL
    url = div.find('div', attrs={'jsname': 'fvi9Ef'}).get('jsdata')
    url = url.split(';')[1]
    
    
    # Fetch each episode and write the file
    podcast = requests.get(url)
    with open(mp3_filename, 'wb') as out:
        out.write(podcast.content)
    
    return name


def mp3_to_wav(mp3_filename, wav_filename):                                                            
    sound = AudioSegment.from_mp3(mp3_filename)
    sound.export(wav_filename, format="wav")


def extract_title_text(url):

    tmp_dir = "out"

    mp3_filename = f"{tmp_dir}/" + "tmp_podcast.mp3"
    wav_filename = f"{tmp_dir}/" + "tmp_podcast.wav"
    txt_filename = f"{tmp_dir}/" + "podcast_tldr.txt"

    Path(tmp_dir).mkdir(parents=True, exist_ok=True)

    title = podcast_title_mp3(url, mp3_filename)
    mp3_to_wav(mp3_filename, wav_filename)
    text = get_transcript(wav_filename, txt_filename, tmp_dir)

    return title, text


def run(url):
    title, text = extract_title_text(url)
    gptldr_core.run(title, text)