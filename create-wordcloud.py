import os
import glob
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud

if __name__ == "__main__":
    # Make sure output dir exists
    os.makedirs("wordclouds", exist_ok=True)

    # Collect all CSV files under data/genre/
    csv_files = glob.glob("data/genre/*.csv")

    # Load and concat all files into one DataFrame
    df_list = []
    for file in csv_files:
        df = pd.read_csv(file)
        df = df[['playlist_name', 'all_spotify_genres']].replace({"'": ""}, regex=True)
        df_list.append(df)
    all_data = pd.concat(df_list, ignore_index=True)

    # Group by playlist_name
    for playlist_name, group in all_data.groupby("playlist_name"):
        # Join all genres for this playlist into one big text blob
        text = ' '.join(group['all_spotify_genres'].dropna().astype(str).tolist())

        if not text.strip():
            continue  # skip empty playlists

        # Generate the word cloud
        wordcloud = WordCloud(
            width=800, height=400, background_color='white'
        ).generate(text)

        # Save to PDF
        out_path = os.path.join("wordclouds", f"{playlist_name}.pdf")

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(out_path, format="pdf")
        plt.close()

        print(f"Saved word cloud for '{playlist_name}' → {out_path}")