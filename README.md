# Anime Downloader

### ABOUT
Anime Downloader is a CLI for downloading HD anime onto your machine. This is for educational purposes only.

### USE
Download all the files and create a virtual environment with the packages specificied in the `requirements.txt`. You can then run `downloader.py`, follow the instructions given in the CLI, and anime will be downloaded based on your internet speed.

FFMPEG IS REQUIRED. PLEASE PLACE FFMPEG INSIDE THE SCRIPTS OF YOUR VIRTUAL ENVIRONMENT.

### HOW IT WORKS
Popular pirated anime sources use `.ts` files to store their video and audio. They use "iframes" to display an HTML5 media player which utilizes `.ts` files for buffering purposes. This script uses a package called "m3u8" to read `.m3u8` files and retrieve the `.ts` file locations. 

```python
for n in network_requests:
    if "master.m3u8" in n["name"]: 
        url = n["name"]

r = requests.get(url)
m3u8_master = m3u8.loads(r.text)
playlist_url = m3u8_master.data["playlists"][0]['uri']
r = requests.get(playlist_url)
playlist = m3u8.loads(r.text)

r = requests.get(playlist.data['segments'][0]['uri'])
```

We then stitch together all these files using basic Python and FFMPEG.
