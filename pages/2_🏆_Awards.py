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

def get_ranking(df, property):
    grouped = df.groupby('user')[property].mean().sort_values(ascending=False)
    return grouped.index.tolist(), grouped.values.tolist()


def show_award(col, property=None, title="Award", reverse=False):
    ranking, vals = get_ranking(df, property)
    if reverse:
        ranking = ranking[::-1]
        vals = vals[::-1]
    
    col.markdown(
        "\n#### {} \n\nš„ **{}** \n\nš„ **{}** \n\nš„ **{}**\n\n\n  &nbsp;".format(title, *ranking[:3])
    )


df = pd.read_csv('data/tracks.csv')
df['user'] = df['user'].map(map_user_names)
df['duration_min'] = df['duration'].apply(lambda x: x / 60)
df['artists'] = df['artists'].apply(lambda x: [a.strip() for a in x[1:-1].replace("'", '').replace('"', '').split(',')])
df['popularity'] = df['popularity'].astype(float)

st.set_page_config(page_title='šµ Playlist', layout='wide')

st.title('šāāļø Unicornication 2022 šāāļø')
st.sidebar.image('unicorn.png')

awards = [
    {'property': 'popularity', 'title': 'š§ Hipster award š§', 'reverse': True},
    {'property': 'duration_min', 'title': 'š Marathon award š', 'reverse': False},
    {'property': 'tempo', 'title': 'šļø Speedcore award šļø', 'reverse': False},
    {'property': 'dancability', 'title': "š I'm a dancer award š", 'reverse': False},
    {'property': 'valence', 'title': 'š§ Emo award š§', 'reverse': True},
    {'property': 'energy', 'title': 'š Red Bull award š', 'reverse': False},
    {'property': 'instrumentalness', 'title': 'š¤ Karaoke award š¤', 'reverse': True},
    {'property': 'liveness', 'title': 'šŖ Festival award šŖ', 'reverse': False},
    {'property': 'loudness', 'title': 'š¢ Volume award š¢', 'reverse': False},
]

award_cols = st.columns(3)
for i, award in enumerate(awards):
    show_award(award_cols[i%len(award_cols)], **award)
