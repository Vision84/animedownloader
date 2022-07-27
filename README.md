# Anime Downloader

### ABOUT
Anime Downloader is a CLI for downloading HD anime onto your machine. This is for educational purposes only.

### USE
Download all the files and create a virtual environment with the packages specificied in the `requirements.txt`. You can then run `downloader.py`, follow the instructions given in the CLI, and anime will be downloaded based on your internet speed.

FFMPEG IS REQUIRED. PLEASE PLACE FFMPEG INSIDE THE SCRIPTS OF YOUR VIRTUAL ENVIRONMENT.

### HOW IT WORKS
Popular pirated anime sources use `.ts` files to store their video and audio. They use "iframes" to display an HTML5 media player which utilizes `.ts` files for buffering purposes. This script uses a package called "m3u8" to read `.m3u8` files and retrieve the `.ts` file locations. We then stitch together all these files using basic Python and FFMPEG.
