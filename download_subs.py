import gzip
import os
import string

import pandas as pd
from pythonopensubtitles import opensubtitles
import requests

import secrets
from imdb_data import DATA_PATH

SUBTITLES_CSV_PATH = os.path.join('data', 'subtitles.csv')


def parse_srt(srt_string):
    line_buffer = []
    captions = []
    lines = srt_string.split('\r\n')
    i = 2
    while i < len(lines):
        if not lines[i]:
            captions.append(' '.join(line_buffer))
            line_buffer = []
            i += 3
        else:
            line_buffer.append(lines[i])
            i += 1
    return captions


def save_sub_entries(sub_entries):
    subs_df = pd.DataFrame(sub_entries, columns=['imdb_id', 'captions'])
    subs_df.to_csv(SUBTITLES_CSV_PATH, index=False)


def main():
    df = pd.read_csv(DATA_PATH)
    os = opensubtitles.OpenSubtitles()
    os.login(secrets.OPENSUBTITLES_USERNAME, secrets.OPENSUBTITLES_PASSWORD)
    sub_entries = []
    for i, row in df.iterrows():
        print(". Processing {} (S{:02}E{:02} ; entry #{})...".format(
            row.series_name, row.season, row.episode, i))
        imdbid = ''.join(c for c in row.imdb_id if c in string.digits)
        results = os.search_subtitles([{'sublanguageid': 'eng', 'imdbid': imdbid}])
        if not results:
            print("   ! No results. Ignoring.")
            continue
        dl_link = results[0]['SubDownloadLink']
        srt_string = gzip.decompress(requests.get(dl_link).content).decode('utf8', errors='ignore')
        captions = parse_srt(srt_string)
        sub_entries.append((row.imdb_id, '\n'.join(captions)))
        if i % 20 == 0:
            save_sub_entries(sub_entries)
            print("   (saved to disk)")
        # print("  - Subtitles : {}".format(captions[:5]))
        # print("")
    save_sub_entries(sub_entries)


if __name__ == '__main__':
    main()
