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

METRIC_MAP = {
    'duur' : {
        'label': 'Lengte',
        'score': '{:.2f} min',
        'delta': '{:.2f} min'
    },
    'tempo' : {
        'label': 'Tempo',
        'score': '{:.0f} bpm',
        'delta': '{:.0f} bpm'
    }, 
    'populariteit' : {
        'label': 'Populariteit',
        'score': '{:.0f}%',
        'delta': '{:.0f}%'
    },
    'dancability' : {
        'label': 'Dancability',
        'score': '{:.0%}',
        'delta': '{:.0%}'
    },
    'energie' : {
        'label': 'Energie',
        'score': '{:.0%}',
        'delta': '{:.0%}'
    },
    'luidheid' : {
        'label': 'Luidheid',
        'score': '{:.0f} dB',
        'delta': '{:.0f} dB'
    },
    'instrumentaalheid' : {
        'label': 'Instrumentaalheid',
        'score': '{:.0%}',
        'delta': '{:.0%}'
    },
    'blijheid' : {
        'label': 'Blijheid',
        'score': '{:.0%}',
        'delta': '{:.0%}'
    },
    'live-heid' : {
        'label': 'Live-heid',
        'score': '{:.0%}',
        'delta': '{:.0%}'
    }
}

df = pd.read_csv('data/tracks.csv')
df['user'] = df['user'].map(NAME_MAP)
df['duration_min'] = df['duration'].apply(lambda x: x / 60)
df['artists'] = df['artists'].apply(lambda x: [a.strip() for a in x[1:-1].replace("'", '').replace('"', '').split(',')])


st.title('🦄🏄‍♂️Unicornication 2022🏄‍♀️🦄')
st.sidebar.image('unicorn.png')

N_COLS = 3
cols = st.columns([1 for _ in range(N_COLS)] + [N_COLS])

selected_user = st.sidebar.selectbox('Select user', df['user'].unique())
selected_feature_name = cols[-1].selectbox('Select feature', FEATURE_GRAPH_MAP.keys())
selected_graph_feature = FEATURE_GRAPH_MAP[selected_feature_name]['x']

filtered_df = df[df['user'] == selected_user]


fig = px.histogram(
    filtered_df, 
    histnorm='percent', 
    **FEATURE_GRAPH_MAP[selected_feature_name]
)
cols[-1].plotly_chart(fig)


for i, (metric_name, metric) in enumerate(METRIC_MAP.items()):
    selected_feature = FEATURE_GRAPH_MAP[metric_name]['x']
    score = filtered_df[selected_feature].mean()
    score_without = df[df['user'] != selected_user][selected_feature].mean()
    score_with = df[selected_feature].mean()

    cols[i%N_COLS].metric(
        metric['label'],
        metric['score'].format(score),
        metric['delta'].format(score - score_without)
    )
