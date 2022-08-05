import streamlit as st
import pandas as pd
import plotly.express as px


NAME_MAP = {
    'rauwedouwe': 'Douwe',
    '1pat8ir5aqzhzvs7ygs1jp8ga': 'Marcel',
    'basmerbel': 'Bas',
    '31hbrww3peprl3puzzaqqf6yfycy': 'Cas',
    'carmenvs': 'Carmen',
    '11140450740': 'Bryan',

}

df = pd.read_csv('data/tracks.csv')
df['user'] = df['user'].map(NAME_MAP)
df['duration_min'] = df['duration'].apply(lambda x: x / 60)
df['artists'] = df['artists'].apply(lambda x: [a.strip() for a in x[1:-1].replace("'", '').replace('"', '').split(',')])

group_by_user = df.groupby('user')
artist_df = df.explode('artists')

st.title('🦄🏄‍♂️Unicornication 2022🏄‍♀️🦄')
st.sidebar.image('unicorn.png')


group_by_artist = artist_df.groupby('artists').count().reset_index()
fig = px.bar(
    group_by_artist.sort_values('track_id', ascending=False).iloc[:15][::-1], 
    y='artists',
    x='track_id',
    title='Artiest',
    orientation='h',

)
st.plotly_chart(fig)