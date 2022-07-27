from helpers import *

import subprocess
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc # selenium driver that bypasses cloudflare
import requests
import m3u8 # popular package for m3u8 files

anime = input("What anime would you like to search for? ")

# initialize a version of chrome that can bypass cloudflare checks
driver = uc.Chrome(use_subprocess=True)
driver.get("https://animetake.tv") # redirect to anime source

# Wait until the search bar or other element is present on page (commonly used throughout the code)
WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-control')))

# find the search bar, enter the user's choice and submit the form
search_bar = driver.find_element(By.CLASS_NAME, "form-control")
search_bar.send_keys(anime + Keys.ENTER)

# Wait
WebDriverWait(driver, timeout=1).until(EC.presence_of_element_located((By.CLASS_NAME, 'latestep_title')))

# find all the anime titles that were returned by the source
results = driver.find_elements(By.CLASS_NAME, 'latestep_title')

titles = [] # used to convert into list

# populate titles list (doesn't use generator for readability)
for r in results:
    e = r.find_element(By.TAG_NAME, 'h4')
    titles.append(e)

# print all titles using a helper function defined in <helpers.py>
for title in titles:
    print(get_text_excluding_children(driver, title).rstrip("\n"))

# get which title the user wants and navigate to that page
chosen_title = titles[int(input("Which title do you want? Enter a number corresponding to the title: ")) - 1]
chosen_title.click()

# Wait
WebDriverWait(driver, timeout=1).until(EC.presence_of_element_located((By.CLASS_NAME, 'anime-title')))

# find all episodes on the page returned
ep_list = driver.find_elements(By.CLASS_NAME, 'anime-title')

episodes = [] # used to convert into list

# populate episodes list (doesn't use generator for readability)
for episode in ep_list:
    if "Episode" in episode.find_element(By.TAG_NAME, 'b').text:
        episodes.append(episode.find_element(By.TAG_NAME, 'b'))
        
for episode in episodes:
    print(episode.text)

# get the user's episode choice and navigate to that page
episode_number = int(input("Which episode do you want? Choose out of the ones on your screen: ")) - 1

chosen_episode = episodes[episode_number]
chosen_episode.click()

# Wait
WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.ID, 'videowrapper_mplayer')))

# select the videos parent tag
videowrapper = driver.find_element(By.ID, 'videowrapper_mplayer')

# get the iframe displaying the video (this source iframes from another source)
iframe = videowrapper.find_element(By.TAG_NAME, 'iframe')
src = iframe.get_attribute("src")

# redirect to that iframe
driver.get(src)

# find another iframe that leads to ACTUAL source
iframe = driver.find_element(By.TAG_NAME, 'iframe')
link = iframe.get_attribute("src")

# redirect to that link
driver.get(link)

# CHECK NETWORK REQUESTS
JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
network_requests = driver.execute_script(JS_get_network_requests)

file_name = f"{anime} Episode {episode_number + 1}" # episode number for file title

url = "" # URL which will change

# START DOWNLOAD PROCESS
print("Downloading...")

# find the master.m3u8 file that will contain all information about bufferable segments
for n in network_requests:
    if "master.m3u8" in n["name"]: 
        url = n["name"]

r = requests.get(url) # get the master.m3u8 file
m3u8_master = m3u8.loads(r.text) # convert to a readable format
playlist_url = m3u8_master.data["playlists"][0]['uri'] # get the URL of the playlist containing all video segments
r = requests.get(playlist_url) # get the playlist file
playlist = m3u8.loads(r.text) # load into readable format

r = requests.get(playlist.data['segments'][0]['uri']) # get the URL of the segments

# start writing video file with python
print("Writing video file...")
with open('video.ts', 'wb') as f:
    for segment in playlist.data['segments']: # go through each segment and write it to the file
        url = segment['uri']
        r = requests.get(url)
        
        f.write(r.content)

for n in network_requests: # reassign url to the master.m3u8 url
    if "master.m3u8" in n["name"]: 
        url = n["name"]

# similar process to video segments above but for audio
r = requests.get(url)
m3u8_master = m3u8.loads(r.text)
playlist_url = m3u8_master.data["media"][1]['uri'] # get audio playlist url
r = requests.get(playlist_url)
playlist = m3u8.loads(r.text)

r = requests.get(playlist.data['segments'][0]['uri']) # get the segments

print("Writing audio file...")

with open('audio.ts', 'wb') as f:
    for segment in playlist.data['segments']: # write each segment to a new file
        url = segment['uri']
        r = requests.get(url)
        
        f.write(r.content)

print("Merging audio and video...")
# use FFMPEG to merge the video.ts and audio.ts file created by Python to an OUTPUT.TS file
subprocess.run(['ffmpeg', '-i', 'video.ts', '-i', 'audio.ts', '-c', 'copy', 'output.ts'])
print("Converting to MP4...")
# use FFMPEG to convert the .ts file to a more conventional .mp4 file
subprocess.run(['ffmpeg', '-i', 'output.ts', f'{file_name}.mp4'])

# delete all the files created other than the output
print("Removing unnecessary files...")
os.remove("video.ts")
os.remove("audio.ts")
os.remove("output.ts")

print("Finished downloading!")

# DONE!