# Anime Downloader

### ABOUT
Anime Downloader is a CLI for downloading HD anime onto your machine. This is for educational purposes only.

### USE
Download all the files and create a virtual environment with the packages specificied in the `requirements.txt`. You can then run `downloader.py`, follow the instructions given in the CLI, and anime will be downloaded based on your internet speed.

FFMPEG IS REQUIRED. PLEASE PLACE FFMPEG INSIDE THE SCRIPTS OF YOUR VIRTUAL ENVIRONMENT.

### HOW IT WORKS
Popular pirated anime sources use `.ts` files to store their video and audio. They use "iframes" to display an HTML5 media player which utilizes `.ts` files for buffering purposes. This script uses a package called "m3u8" to read `.m3u8` files and retrieve the `.ts` file locations. 

    for n in network_requests:
    if "master.m3u8" in n["name"]: 
        url = n["name"]

    r = requests.get(url) # get the master.m3u8 file
    m3u8_master = m3u8.loads(r.text) # convert to a readable format
    playlist_url = m3u8_master.data["playlists"][0]['uri'] # get the URL of the playlist containing all video segments
    r = requests.get(playlist_url) # get the playlist file
    playlist = m3u8.loads(r.text) # load into readable format

    r = requests.get(playlist.data['segments'][0]['uri']) # get the URL of the segments

We then stitch together all these files using basic Python and FFMPEG.
