# -*- coding: utf-8 -*-
"""Spotify 2023 analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FBRYsecbsV00ThKMnpTnLj3_myLwC1mA
"""

import numpy as np
import pandas as pd # for data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

"""# 1. Importing the data"""

# importing dataset using 'ISO-8859-1' encoding
spotify_data = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Displaying the first few rows of the dataset
spotify_data.head()

"""# 2. Basic stats"""

data_summary = spotify_data.describe(include='all')
data_summary

# Checking for missing values in the dataset
missing_values = spotify_data.isnull().sum()

# Displaying the count of missing values for each column
missing_values

"""# 3. Distribution of percentage features"""

sns.set_style("whitegrid")

# Creating a list of features to visualize
features_to_visualize = ['danceability_%', 'energy_%', 'valence_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']

# Setting up the figure and axes
fig, axes = plt.subplots(nrows=len(features_to_visualize), figsize=(12, 15))

# Plotting the distribution for each feature
for i, feature in enumerate(features_to_visualize):
    sns.histplot(spotify_data[feature], ax=axes[i], bins=30, kde=True)
    axes[i].set_title(f'Distribution of {feature}', fontsize=14)
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

"""# 4. The top 10 songs based on their presence in Spotify playlists"""

# Selecting the top 10 songs based on their presence in Spotify playlists
top_songs_in_playlists = spotify_data.sort_values(by='in_spotify_playlists', ascending=False).head(10)

# Creating a combined column for track and artist name for better visualization
top_songs_in_playlists['track_artist'] = top_songs_in_playlists['track_name'] + " (" + top_songs_in_playlists['artist(s)_name'] + ")"

# Plotting the songs with artist names
plt.figure(figsize=(12, 10))
sns.barplot(x=top_songs_in_playlists['in_spotify_playlists'], y=top_songs_in_playlists['track_artist'],
            palette="viridis", orient='h')
plt.title('Top 10 Songs Based on Presence in Spotify Playlists', fontsize=16)
plt.xlabel('Number of Playlists')
plt.ylabel('Track (Artist)')
plt.tight_layout()
plt.show()

"""# 5. Top 10 artists based on total streams"""

# Converting 'streams' column to numeric data type
spotify_data['streams'] = pd.to_numeric(spotify_data['streams'], errors='coerce')

# Grouping by artist(s) again and summing up their streams
artist_streams = spotify_data.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10)

# Plotting the artists with the most streams again
plt.figure(figsize=(12, 10))
sns.barplot(x=artist_streams.values, y=artist_streams.index, palette="viridis", orient='h')
plt.title('Top 10 Artists Based on Total Streams', fontsize=16)
plt.xlabel('Total Streams (in billions)')
plt.ylabel('Artist(s) Name')
plt.tight_layout()
plt.show()

"""# 6. Streams vs percentage features"""

# List of features to compare with streams
features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'liveness_%', 'speechiness_%']

# Setting up the figure and axes
fig, axes = plt.subplots(nrows=len(features), figsize=(12, 20))

# Plotting scatter plots and printing correlation coefficients for each feature
correlations = {}
for i, feature in enumerate(features):
    sns.scatterplot(x=spotify_data[feature], y=spotify_data['streams'], ax=axes[i], alpha=0.6)
    axes[i].set_title(f'Streams vs. {feature}', fontsize=14)
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel('Streams')
    corr = spotify_data['streams'].corr(spotify_data[feature])
    correlations[feature] = corr
    axes[i].annotate(f'Correlation: {corr:.2f}', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=12)

plt.tight_layout()
plt.show()

correlations

"""***Streams vs. Danceability***: A slightly negative correlation (r=−0.105) suggests that tracks with higher danceability tend to have slightly fewer streams, although the relationship is weak.

***Streams vs. Valence***: A very weak negative correlation (r=−0.041), implying that the mood of the track (from sad to happy) has little influence on the number of streams.

***Streams vs. Energy***: An even weaker negative correlation (r=−0.026), suggesting that the energy of a track has minimal impact on its streams.

***Streams vs. Acousticness***: Almost no correlation (r=−0.004), indicating that the acousticness of a track doesn't significantly influence its streams.

***Streams vs. Liveness***: A weak negative correlation (r=−0.048), suggesting that tracks recorded live might have slightly fewer streams.

***Streams vs. Speechiness***: A slightly negative correlation (r=−0.112), suggesting that tracks with more spoken words or rap might have slightly fewer streams.

# 7. Percentage features vs top artists
"""

# Selecting the top 10 artists based on the number of songs they have in the dataset
top_artists = spotify_data['artist(s)_name'].value_counts().head(10).index

# Filtering the dataset to include only these top artists
top_artists_data = spotify_data[spotify_data['artist(s)_name'].isin(top_artists)]

# Setting up the figure and axes
fig, axes = plt.subplots(nrows=len(features), figsize=(12, 20))

# Plotting average values for each feature for the top artists
for i, feature in enumerate(features):
    artist_feature_avg = top_artists_data.groupby('artist(s)_name')[feature].mean().sort_values(ascending=False)
    sns.barplot(x=artist_feature_avg.values, y=artist_feature_avg.index, ax=axes[i], palette="viridis")
    axes[i].set_title(f'Average {feature} for Top Artists', fontsize=14)
    axes[i].set_xlabel(f'Average {feature}')
    axes[i].set_ylabel('Artist(s) Name')

plt.tight_layout()
plt.show()

"""# 8. Temporal analysis"""

# Checking unique values for 'released_year', 'released_month', and 'released_day'
unique_values = {
    'released_year': spotify_data['released_year'].unique(),
    'released_month': spotify_data['released_month'].unique(),
    'released_day': spotify_data['released_day'].unique()
}


# Creating a 'release_date_string' column
spotify_data['release_date_string'] = spotify_data['released_year'].astype(str) + '-' + \
                                      spotify_data['released_month'].astype(str) + '-' + \
                                      spotify_data['released_day'].astype(str)

# Converting the 'release_date_string' column to datetime data type
spotify_data['release_date'] = pd.to_datetime(spotify_data['release_date_string'], errors='coerce')

# Rechecking the distribution of song releases by year
yearly_releases = spotify_data['release_date'].dt.year.value_counts().sort_index()

# Plotting the distribution of song releases by year
plt.figure(figsize=(14, 7))
yearly_releases.plot(kind='bar', color='skyblue')
plt.title('Distribution of Song Releases by Year', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Songs Released')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculating yearly averages for streams, danceability, and energy
yearly_averages = spotify_data.groupby(spotify_data['release_date'].dt.year)[['streams', 'danceability_%', 'energy_%']].mean()

# Plotting the yearly trends
fig, axes = plt.subplots(nrows=3, figsize=(14, 15))

# Average Streams by Year
axes[0].plot(yearly_averages.index, yearly_averages['streams'], marker='o', color='teal')
axes[0].set_title('Yearly Trend in Average Streams', fontsize=16)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Average Streams')
axes[0].grid(True)

# Average Danceability by Year
axes[1].plot(yearly_averages.index, yearly_averages['danceability_%'], marker='o', color='purple')
axes[1].set_title('Yearly Trend in Average Danceability', fontsize=16)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Average Danceability (%)')
axes[1].grid(True)

# Average Energy by Year
axes[2].plot(yearly_averages.index, yearly_averages['energy_%'], marker='o', color='orange')
axes[2].set_title('Yearly Trend in Average Energy', fontsize=16)
axes[2].set_xlabel('Year')
axes[2].set_ylabel('Average Energy (%)')
axes[2].grid(True)

plt.tight_layout()
plt.show()

"""# 9. Comparison across platforms"""

spotify_data['in_spotify_playlists']

spotify_data['in_deezer_playlists']

# Calculating the total count of tracks present in playlists/charts for Spotify and Apple Music
total_counts = {
    'Spotify': spotify_data['in_spotify_playlists'].sum() + spotify_data['in_spotify_charts'].sum(),
    'Apple Music': spotify_data['in_apple_playlists'].sum() + spotify_data['in_apple_charts'].sum(),
}

# Plotting the total count comparison for Spotify and Apple Music
plt.figure(figsize=(10, 7))
plt.bar(total_counts.keys(), total_counts.values(), color=['green', 'red'])
plt.title('Total Count of Tracks in Playlists/Charts: Spotify, Apple Music, Deezer', fontsize=16)
plt.ylabel('Total Count')
plt.xlabel('Platform')
plt.tight_layout()
plt.show()

# Identifying top 10 songs for Spotify based on their presence in playlists and charts
top_songs_spotify = spotify_data[['track_name', 'artist(s)_name', 'in_spotify_playlists', 'in_spotify_charts']]
top_songs_spotify['spotify_total'] = top_songs_spotify['in_spotify_playlists'] + top_songs_spotify['in_spotify_charts']
top_songs_spotify = top_songs_spotify.sort_values(by='spotify_total', ascending=False).head(10)

# Identifying top 10 songs for Apple Music based on their presence in playlists and charts
top_songs_apple = spotify_data[['track_name', 'artist(s)_name', 'in_apple_playlists', 'in_apple_charts']]
top_songs_apple['apple_total'] = top_songs_apple['in_apple_playlists'] + top_songs_apple['in_apple_charts']
top_songs_apple = top_songs_apple.sort_values(by='apple_total', ascending=False).head(10)

top_songs_spotify

top_songs_apple

# Setting up the figure and axes
fig, axes = plt.subplots(nrows=2, figsize=(12, 15))

# Plotting the top 10 songs for Spotify
sns.barplot(x=top_songs_spotify['spotify_total'], y=top_songs_spotify['track_name'] + " (" + top_songs_spotify['artist(s)_name'] + ")",
            palette="viridis", ax=axes[0])
axes[0].set_title('Top 10 Songs on Spotify Based on Presence in Playlists/Charts', fontsize=16)
axes[0].set_xlabel('Total Presence')
axes[0].set_ylabel('Track (Artist)')

# Plotting the top 10 songs for Apple Music
sns.barplot(x=top_songs_apple['apple_total'], y=top_songs_apple['track_name'] + " (" + top_songs_apple['artist(s)_name'] + ")",
            palette="viridis", ax=axes[1])
axes[1].set_title('Top 10 Songs on Apple Music Based on Presence in Playlists/Charts', fontsize=16)
axes[1].set_xlabel('Total Presence')
axes[1].set_ylabel('Track (Artist)')

plt.tight_layout()
plt.show()

"""# 10. Artists collaborations"""

# Identifying collaborations by splitting the 'artist(s)_name' column
spotify_data['artists_list'] = spotify_data['artist(s)_name'].str.split(', ')

# Filtering out songs that have only one artist to get collaborative tracks
collaborations = spotify_data[spotify_data['artists_list'].apply(len) > 1]

# Displaying the first few rows of the collaborations dataframe
collaborations[['track_name', 'artist(s)_name', 'streams', 'in_spotify_playlists', 'in_spotify_charts']].head()

# Function to get all combinations of artists for each track
def get_artist_combinations(artists_list):
    return list(combinations(sorted(artists_list), 2))

# Apply the function to the 'artists_list' column to get all artist combinations
collaborations['artist_combinations'] = collaborations['artists_list'].apply(get_artist_combinations)

# Flatten the list of artist combinations to count the frequency of each combination
all_combinations = [combo for sublist in collaborations['artist_combinations'] for combo in sublist]
frequent_collaborators = pd.Series(all_combinations).value_counts().head(10)

# Plotting the top 10 frequent collaborator pairs
plt.figure(figsize=(12, 8))
sns.barplot(x=frequent_collaborators.values, y=frequent_collaborators.index, palette="viridis")
plt.title('Top 10 Frequent Collaborator Pairs', fontsize=16)
plt.xlabel('Number of Collaborations')
plt.ylabel('Artist Pairs')
plt.tight_layout()
plt.show()

# Calculating average streams and presence in playlists for collaborative tracks
collab_avg_streams = collaborations['streams'].mean()

# Calculating average streams and presence in playlists for all tracks
overall_avg_streams = spotify_data['streams'].mean()

# Creating a DataFrame to visualize the comparison
data = {
    'Metrics': ['Average Streams'],
    'Collaborations': [collab_avg_streams],
    'Overall': [overall_avg_streams]
}
comparison_df = pd.DataFrame(data).melt(id_vars=['Metrics'], value_vars=['Collaborations', 'Overall'])

# Plotting the comparison
plt.figure(figsize=(12, 7))
sns.barplot(x='Metrics', y='value', hue='variable', data=comparison_df, palette="viridis")
plt.title('Comparison of Streams: Collaborations vs. Overall', fontsize=16)
plt.xlabel('')
plt.ylabel('')
plt.legend(title='')
plt.tight_layout()
plt.show()

# Recalculating the average Spotify presence for collaborative tracks and overall tracks
collab_avg_spotify_presence = (collaborations['in_spotify_playlists'] + collaborations['in_spotify_charts']).mean()
overall_avg_spotify_presence = (spotify_data['in_spotify_playlists'] + spotify_data['in_spotify_charts']).mean()

# Plotting the comparison for Average Spotify Presence
labels = ['Collaborations', 'Overall']
values = [collab_avg_spotify_presence, overall_avg_spotify_presence]

plt.figure(figsize=(10, 7))
sns.barplot(x=labels, y=values, palette="viridis")
plt.title('Average Spotify Presence: Collaborations vs. Overall', fontsize=16)
plt.ylabel('Average Presence')
plt.tight_layout()
plt.show()

