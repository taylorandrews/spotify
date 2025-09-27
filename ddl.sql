DROP TABLE IF EXISTS track;

CREATE TABLE track (
    album_album varchar(1000),
    album_href varchar(1000),
    album_id varchar(1000),
    album_name varchar(1000),
    album_release varchar(1000),
    album_type varchar(1000),
    album_uri varchar(1000),
    all_spotify_genres varchar(1000),
    artist_id varchar(1000),
    artist_name varchar(1000),
    artist_type varchar(1000),
    artist_uri varchar(1000),
    disc_number varchar(1000),
    duration_ms varchar(1000),
    episode varchar(1000),
    explicit varchar(1000),
    id varchar(1000),
    is_local varchar(1000),
    name varchar(1000),
    playlist_name varchar(1000),
    popularity varchar(1000),
    track varchar(1000),
    track_number varchar(1000),
    type varchar(1000),
    uri varchar(1000),
    count_in_playlist varchar(1000)
);


\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_0.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_5.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_10.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_15.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_20.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_25.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_30.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_35.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_40.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_45.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_50.csv' WITH CSV HEADER;
\copy playlist_tracks FROM '/Users/taylor/Documents/projects/coding-fun/spotify/data/playlist_tracks_55.csv' WITH CSV HEADER;

