import os
import json
import math
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

@st.cache
def get_spotipy_class():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist(playlist_id)['tracks']
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def preprocess_playlist_data(playlist):
    track_with_features = [x.split('.')[0] for x in os.listdir('data/track_features')]

    tracks_info = []
    for i, track in enumerate(playlist):
        track_dict = {
            'track_id': track['track']['id'],
            'user': track['added_by']['id'],
            'name': track['track']['name'],
            'artists': [artist['name'] for artist in track['track']['artists']],
            'duration': track['track']['duration_ms'] / 1000,
            'is_explicit': track['track']['explicit'],
            'popularity': track['track']['popularity'],
            'has_track_features': False,
        }

        if track_dict['track_id'] in track_with_features:
            features = json.load(open('data/track_features/{}.json'.format(track_dict['track_id'])))

            track_dict['dancability'] = features['danceability']
            track_dict['energy'] = features['energy']
            track_dict['loudness'] = features['loudness']
            track_dict['tempo'] = features['tempo']
            track_dict['speechiness'] = features['speechiness']
            track_dict['acousticness'] = features['acousticness']
            track_dict['instrumentalness'] = features['instrumentalness']
            track_dict['valence'] = features['valence']
            track_dict['liveness'] = features['liveness']

            track_dict['has_track_features'] = True
        tracks_info.append(track_dict)

    df = pd.DataFrame(tracks_info)
    df.to_csv('data/tracks.csv', index=False)
    return df

def request_track_features(sp, df):
    tracks_to_request = list(set(df[df['has_track_features'] == False]['track_id']))

    for i in range(math.ceil(float(len(tracks_to_request)) / 100)):
        batch = tracks_to_request[i * 100: (i + 1) * 100]

        features = sp.audio_features(batch)
        for feature in features:
            json.dump(feature, open('data/track_features/{}.json'.format(feature['id']), 'w'))


with st.expander("Query the Spotify API"):
    text_box = st.text_input("Wachtwoord:")
    if text_box == "wachtwoord":
        with st.spinner("Loading..."):
            sp = get_spotipy_class()
            playlist = get_playlist_tracks(sp, '5oRHsgBoMQk54LpCt0na9J')
            df_tracks = preprocess_playlist_data(playlist)
            request_track_features(sp, df_tracks)
            df_tracks = preprocess_playlist_data(playlist)


        