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
    'hankmoody420': 'Han'
}
def map_user_names(name):
    if name in NAME_MAP:
        return NAME_MAP[name]
    else:
        return name

df = pd.read_csv('data/tracks.csv')
df['user'] = df['user'].map(map_user_names)
df['duration_min'] = df['duration'].apply(lambda x: x / 60)
df['artists'] = df['artists'].apply(lambda x: [a.strip() for a in x[1:-1].replace("'", '').replace('"', '').split(',')])

group_by_user = df.groupby('user')
artist_df = df.explode('artists')

st.title('🏄‍♂️ Unicornication 2022 🏄‍♀️')
st.sidebar.image('unicorn.png')

col1, col2 = st.columns(2)
counts_per_user = group_by_user.count().reset_index()
fig = px.bar(
    counts_per_user.sort_values('duration_min', ascending=False)[::-1], 
    y='user',
    x='track_id',
    title='Aantal tracks per persoon',
    orientation='h',

)
col1.plotly_chart(fig, use_container_width=True)

summed_per_user = group_by_user.sum().reset_index()
fig = px.bar(
    summed_per_user.sort_values('duration_min', ascending=False)[::-1], 
    y='user',
    x='duration_min',
    title='Totale lengte per persoon',
    orientation='h',

)
col2.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
group_by_artist = artist_df.groupby('artists').count().reset_index()
fig = px.bar(
    group_by_artist.sort_values('track_id', ascending=False).iloc[:15][::-1], 
    y='artists',
    x='track_id',
    title='Aantal tracks per artiest',
    orientation='h',

)
col1.plotly_chart(fig, use_container_width=True)

group_by_artist = artist_df.groupby('artists').sum().reset_index()
fig = px.bar(
    group_by_artist.sort_values('duration_min', ascending=False).iloc[:15][::-1], 
    y='artists',
    x='duration_min',
    title='Totale lengte per artiest',
    orientation='h',

)
col2.plotly_chart(fig, use_container_width=True)