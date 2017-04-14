import pandas as pd

import lxml.etree
import glob
import os

XML_GLOB_PATTERN = os.path.join('data', 'OpenSubtitles2016', 'xml', 'en', '1999', '*', '*.xml')


def main():
    print("- Exploring subdirs to find all XML files.")
    paths = glob.glob(XML_GLOB_PATTERN)
    for path in paths:
        print("  * Processing '{}'...".format(path))
        tokens = path.split(os.path.sep)
        year = tokens[4]

        with open(path) as xml_file:
            xml_tree = lxml.etree.parse(xml_file)
            sentences = xml_tree.xpath('//s')
            subtitles = '\n'.join(' '.join(w.text for w in s.xpath('//w')) for s in sentences)
            print(path)
            print(subtitles[:100])


if __name__ == '__main__':
    main()
