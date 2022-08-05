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

FEATURE_GRAPH_MAP = {
    'duur' : {
        'x': 'duration_min',
        'title': 'Duur',
        'range_x': [0, None],
        'labels': {'duration_min': 'Lengte (min)'}
    },
    'tempo' : {
        'x': 'tempo',
        'title': 'Tempo',
        'labels': {'tempo': 'tempo (bpm)'}
    }, 
    'populariteit' : {
        'x': 'popularity',
        'title': 'Populariteit',
        'range_x': [0, 100],
        'labels': {'popularity': 'populariteit'}
    },
    'dancability' : {
        'x': 'dancability',
        'title': 'Dancability',
        'range_x': [0, 1],
        'labels': {'dancability': 'dancability'}
    },
    'energie' : {
        'x': 'energy',
        'title': 'Energie',
        'range_x': [0, 1],
        'labels': {'energy': 'energie'}
    },
    'luidheid' : {
        'x': 'loudness',
        'title': 'Luidheid',
        'labels': {'loudness': 'luidheid (dB)'}
    },
    'instrumentaalheid' : {
        'x': 'instrumentalness',
        'title': 'Instrumentaalheid',
        'range_x': [0, 1],
        'labels': {'instrumentalness': 'instrumentaalheid'}
    },
    'blijheid' : {
        'x': 'valence',
        'title': 'Blijheid',
        'range_x': [0, 1],
        'labels': {'valence': 'blijheid'}
    },
    'live-heid' : {
        'x': 'liveness',
        'title': 'Live-heid',
        'range_x': [0, 1],
        'labels': {'liveness': 'live-heid'}
    }
}

df = pd.read_csv('data/tracks.csv')
df['user'] = df['user'].map(NAME_MAP)
df['duration_min'] = df['duration'].apply(lambda x: x / 60)
df['artists'] = df['artists'].apply(lambda x: [a.strip() for a in x[1:-1].replace("'", '').replace('"', '').split(',')])
df['popularity'] = df['popularity'].astype(float)

st.set_page_config(page_title='🎵 Playlist', layout='wide')
st.title('🦄🏄‍♂️Unicornication 2022🏄‍♀️🦄')
st.sidebar.image('unicorn.png')

selected_user = st.sidebar.multiselect('Selecteer gebruiker', df['user'].unique(), default=df['user'].unique())
selected_feature = st.sidebar.selectbox('Kies een eigenschap', sorted(list(FEATURE_GRAPH_MAP.keys())))

filtered_df = df[['user', 'name', 'artists', FEATURE_GRAPH_MAP[selected_feature]['x']]]
filtered_df = filtered_df[filtered_df['user'].isin(selected_user)]


st.dataframe(filtered_df)

fig = px.histogram(
    filtered_df, 
    histnorm='percent', 
    **FEATURE_GRAPH_MAP[selected_feature]
)
st.plotly_chart(fig)


