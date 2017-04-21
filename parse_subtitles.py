import pandas as pd

import lxml.etree
import glob
import os

XML_SUBTITLES_GLOB = os.path.join('data', 'OpenSubtitles2016', 'xml', 'en', '2010', '*', '*.xml')
DATA_PATH = os.path.join('data', 'parsed_subtitles.csv')
METADATA_TAGS = ['country', 'duration', 'genre']
COLUMNS = ['id', 'year', 'subtitles'] + METADATA_TAGS


def save_entries(entries):
    df = pd.DataFrame(entries, columns=COLUMNS)
    df.to_csv(DATA_PATH, index=False)


def main():
    print("- Exploring subdirs to find all XML files.")
    entries = []
    paths = glob.glob(XML_SUBTITLES_GLOB)
    print("- Beginning XML parsing:")
    for path in paths:
        tokens = path.split(os.path.sep)
        sub_id, year = tokens[-1].split('.')[0], tokens[-3]
        with open(path) as xml_file:
            xml_tree = lxml.etree.parse(xml_file)
            subtitles = [w.text for w in xml_tree.iterfind('s/w')]
            entry = [sub_id, year, subtitles]
            metadata = (xml_tree.find('/meta/source/{}'.format(m_tag))
                        for m_tag in METADATA_TAGS)
            entry += [m.text if m is not None else None for m in metadata]
            entries.append(tuple(entry))
            if len(entries) % 500 == 0:
                print("  * Processed {}/{} files. Sample: '{}'...".format(len(entries), len(paths),
                                                                          subtitles[:10]))
            if len(entries) % 5000 == 0:
                print("  ! Saving current entries.")
                save_entries(entries)
    save_entries(entries)
    print("! Processing complete! Entries saved.")


if __name__ == '__main__':
    main()
