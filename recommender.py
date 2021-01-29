import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector


def connect_to_db():
    db = mysql.connector.connect(user='group3',
                                 password='ZCW+G3+data1-2',
                                 host='ls-981afae8457656b0e311a4599e509521975ea3c7.c13c4sg7cvg0.us-east-2.rds.amazonaws.com',
                                 database='group3'
                                 )
    return db


def get_trending_video_data():
    db = connect_to_db()
    query = '''SELECT * FROM youtube'''
    df = pd.read_sql(query, con=db)
    df['related_description'] = ''
    df['related_tags'] = ''
    return df


def get_related_video_data():
    db = connect_to_db()
    query = '''SELECT * FROM related_videos'''
    df = pd.read_sql(query, con=db)
    df['tags'].replace('[]', '', inplace=True)
    return df


def clean_tags(df):
    df['tags'] = df['tags'].str.replace('|', ' ')


def add_related_video_metadata():
    related = get_related_video_data()
    clean_tags(related)
    trending_df = get_trending_video_data()
    unique_ids = related['related_vid_id'].unique()
    for i in unique_ids:
        related_df = related.loc[related['related_vid_id'] == i]
        related_description = related_df['description'].str.cat(sep=' ')
        related_tags = related_df['tags'].str.cat(sep=' ')
        trending_df.loc[trending_df['video_id'] == i, 'related_description'] = related_description
        trending_df.loc[trending_df['video_id'] == i, 'related_tags'] = related_tags
    return trending_df


def create_soup(x):
    # return x['description'] + x['tags']
    return x['description'] + x['tags'] + x['related_description'] + x['related_tags']


# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', 10)
tfidf = TfidfVectorizer(stop_words='english')
metadata = add_related_video_metadata()
metadata['description'] = metadata['description'].fillna('')
metadata['tags'] = metadata['tags'].str.replace('|', ' ')
metadata['soup'] = metadata.apply(create_soup, axis=1)
metadata.drop_duplicates()
tfidf_matrix = tfidf.fit_transform(metadata['soup'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(metadata.index, index=metadata['video_id']).drop_duplicates()


def get_recommendations(video_id, cosine_sim=cosine_sim):
    idx = indices[video_id]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    video_indices = [i[0] for i in sim_scores]
    print(metadata[['video_id', 'title']].loc[metadata['video_id'] == video_id])
    return metadata[['video_id', 'title']].iloc[video_indices]


print(get_recommendations('_n-6a0UPvSQ'))
