# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 01:19:37 2020

@author: Alexander Merolla
"""

'''
Example of segments data fetched from analysis:

"segments": [{"start": 0.0, "duration": 0.24404, "confidence": 0.0, "loudness_start": -60.0, "loudness_max_time": 0.0, "loudness_max": -60.0, "loudness_end": 0.0, "pitches": [1.0, 0.335, 0.281, 0.168, 0.314, 0.23, 0.276, 0.409, 0.1, 0.111, 0.152, 0.297], "timbre": [0.0, 171.13, 9.469, -28.48, 57.491, -50.067, 14.833, 5.359, -27.228, 0.973, -10.64, -7.228]}, {"start": 0.24404, "duration": 0.17891, "confidence": 0.448, "loudness_start": -60.0, "loudness_max_time": 0.14031, "loudness_max": -53.992, "loudness_end": 0.0, 
'''

import os
import json
import time
import spotipy
import spotipy.util as util

class sp:
    
    def __init__(self, username):
        self.username = username
        self.auth_user()
        self.get_current_song_data()
        if self.songID != None:
            self.get_analysis()
            self.parse_song_analysis()
    
    timestamp = None
    progress = None
    last_progress = None
    is_playing = None
    songID = None
    last_songID = None
    analysis = None
    scope = None
    token = None
    spotifyObject = None
    song_library = None
    current_song_data = None
    current_loudness = None
    segment_pos = None
    loudness_arr = []
    segments_arr = []
    bars_confidence_arr = []
    bars_start_arr = []
    tatums_confidence_arr = []
    tatums_start_arr = []
    beats_start_arr = []
    beats_confidence_arr = []

    '''
    Create a song cache libary if one does not already exist
    This folder will store the analysis of every song played
    in JSON format
    '''
    song_library = os.getcwd() + '\\' + 'songs'
    if os.path.exists(song_library) == False:
        os.mkdir(song_library)
    

    '''
    Scope will define the permissions of this spotify application
    '''
    scope = ('user-read-currently-playing '
    + 'user-read-playback-state '
    + 'user-modify-playback-state '
    + 'user-library-read '
    + 'user-top-read '
    + 'user-read-playback-position '
    + 'user-read-recently-played '
    + 'user-follow-read '
    )

    ''' 
    Clear authentication cache if authentication doesn't work
    '''
    def auth_user(self):
        try:
            self.token = util.prompt_for_user_token(self.username,scope=self.scope)
            self.spotifyObject = spotipy.Spotify(auth=self.token)
        except:
            os.remove(f"cache-(username)")
            self.token = util.prompt_for_user_token(self.username)
            self.spotifyObject = spotipy.Spotify(auth=self.token)
    
    '''
    Cache song analysis with the Song ID (as given by Spotify) 
    '''
    def dump_json(self):
        temp = json.dumps(self.analysis)
        f = open(self.song_library + '\\' + self.songID, 'w')
        f.write(temp)
        f.close()
        
    '''
    Check if the current song exists in cache before requesting
    from the Spotify API
    '''
    def get_analysis(self):
        if self.songID != None:
            if os.path.exists(self.song_library + '\\' + self.songID):
                with open(self.song_library + '\\' + self.songID) as f:
                    self.analysis = json.load(f)
            else:
                self.analysis = self.spotifyObject.audio_analysis(self.songID)
                self.dump_json()

    '''
    Collect relevant song information from the current playing song
    '''
    def get_current_song_data(self):
        self.current_song_data = self.spotifyObject.current_user_playing_track()
        if self.current_song_data != None:
            self.timestamp = time.time()
            self.songID = self.current_song_data['item']['id']
            self.last_progress = self.progress
            self.progress = self.current_song_data['progress_ms'] / 1000.0
            self.is_playing = self.current_song_data['is_playing']

    '''
    Run through the song analysis to parse the loudness, start,
    confidence, tatums, beats, and bars
    '''                   
    def parse_song_analysis(self):
        for entry in self.analysis['segments']:
            self.loudness_arr.append(entry['loudness_max'])
            self.segments_arr.append(entry['start'])
        for entry in self.analysis['bars']:
            self.bars_start_arr.append(entry['start'])
            self.bars_confidence_arr.append(entry['confidence'])
        for entry in self.analysis['tatums']:
            self.tatums_start_arr.append(entry['start'])
            self.tatums_confidence_arr.append(entry['confidence'])
        for entry in self.analysis['beats']:
            self.beats_start_arr.append(entry['start'])
            self.beats_confidence_arr.append(entry['confidence'])
    
    '''
    Check if a song is currently playing
    '''
    def is_Playing(self):
        if self.current_song_data != None and self.current_song_data['is_playing'] != False:
            return True
        else:
            return False

    '''
    Use the current time to find the correct segment of the song
    ''' 
    def get_segment_pos(self):
            for position, value in enumerate(self.segments_arr[::-1]):
                if ((time.time() - self.timestamp) + self.progress) >= value:
                    self.segment_pos = len(self.segments_arr) - position - 1
                    return self.segment_pos
            return None
    
    def bar_pos(self):
        for position, value in enumerate(self.bars_start_arr[::-1]):
            if ((time.time() - self.timestamp) + self.progress) >= value:
                return len(self.bars_start_arr) - position - 1
        return None
    
    def tatum_pos(self):
        for position, value in enumerate(self.tatums_start_arr[::-1]):
            if ((time.time() - self.timestamp) + self.progress) >= value:
                return len(self.tatums_start_arr) - position - 1
        return None
    
    def beat_pos(self):
        for position, value in enumerate(self.beats_start_arr[::-1]):
            if ((time.time() - self.timestamp) + self.progress) >= value:
                return len(self.beats_start_arr) - position - 1
        return None
    
    '''
    Update will update all relevant song information including the current song data,
    fetching analysis if required and parsing the song analysis
    '''
    def update(self, update_rate_s = 1):
        if time.time() - self.timestamp > update_rate_s:
            self.get_current_song_data()
            if self.songID != self.last_songID and self.songID != None:
                self.last_songID = self.songID
                self.get_analysis()
                self.parse_song_analysis()
        if self.songID != None:
            self.get_segment_pos()
        return None
    
    '''
    Crudely converts dB scale to an amplitude between 0-1
    '''
    def db_amp(self):
        db = self.loudness_arr[self.segment_pos]
        db = 10**(db/20)
        if db > 1:
            return 1
        else:
            return db
    
    '''
    Scale the amplitude based on the current beat volume

    If the current volume is less than the bar height,
    decrement by <decrement_db> for a smoother animation

    <min_db> is the minimum decibel for the bar to activate

    <beat_confidence> minimum amount of confidence required
    to be counted as a beat
    '''
    def beat_bar(self, beat_confidence = 0.2, decrement_db = 0.125, min_db = 0.1):
        current_bar = 0
        db_scaled = 0
        while True:
            if current_bar != self.beats_start_arr[self.beat_pos()] and self.beats_confidence_arr[self.beat_pos()] > beat_confidence and self.db_amp() > min_db:
                current_bar = self.beats_start_arr[self.beat_pos()]
                db_scaled = self.db_amp()
                yield db_scaled
            else:
                db_scaled -= decrement_db
                if db_scaled < 0:
                    db_scaled = 0
            yield db_scaled
    
if __name__ == '__main__':
    test = sp('place_username_here')
    print('Success!')
        

            
                                                                                                                                                                                                                                                                                                                                                         
            
        
    