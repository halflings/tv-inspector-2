import os

from imdbpie import Imdb
import lxml.html
import pandas as pd
import requests

EZTV_URL = 'https://eztv.unblocked.fyi/showlist/rating/'
DATA_PATH = os.path.join('data', 'imdb.csv')


def main():
    print("! Getting a list of TV shows from eztv...")
    showlist_page = lxml.html.fromstring(requests.get(EZTV_URL).content)
    shows = [l.text for l in showlist_page.xpath('//a[@class="thread_link"]')]
    print("")
    imdb = Imdb()
    episode_records = []
    for show_name in shows[:10]:
        print("* Processing `{}`...".format(show_name))
        episodes = None
        for show in imdb.search_for_title(show_name):
            try:
                episodes = imdb.get_episodes(show['imdb_id'])
                break
            except (RuntimeError, TypeError):
                # RuntimeError: This is thrown when a show is not recognized a series
                # TypeError: Bug where seasons is None.
                continue
        if episodes is None:
            print("  ! Couldn't find an IMDB entry for `{}`. Ignoring.".format(show_name))
            continue
        episode_records += [e.__dict__ for e in episodes]
    df = pd.DataFrame(episode_records)
    df.to_csv(DATA_PATH, index=False)


if __name__ == '__main__':
    main()
