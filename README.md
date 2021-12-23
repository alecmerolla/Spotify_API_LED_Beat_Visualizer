# Spotify_API_LED_Beat_Visualizer

Repository for a Spotify LED (WS2812) beat visualizer. This app uses the Spotify API to change the magnitude of any WS2812 led strip or matrix based on the beat of the song currently being played. Variables for beat confidence and activation height are included. To avoid rate limiting on API usage included in the standard premium account, I've decided to cache the analysis of every song played.

In light of finding out that Spotify has a API that provides a mountain of data on every song in their libarary, I decided to create a small application to parse and find use for some of the data available to its users. This application was designed for a Raspberry PI 3, although the libary could be used for any application using the Spotify song analysis data. 

To get started, you will need to follow the documentation in the Spotipy API to get a SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in order for the app to login under your username. These variables will need to be set as environmental variables on whichever system you are using. You can find details here:
https://spotipy.readthedocs.io/en/2.19.0/

Lastly, you will need to install the rpi_ws281x python library to run the WS2812 or similar LEDs. Link here: https://pypi.org/project/rpi-ws281x/1.1.3/
