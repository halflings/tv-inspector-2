# Create a data directory
mkdir data
# Download the dataset
curl http://opus.lingfil.uu.se/OpenSubtitles2016/en.tar.gz > "data/en.tar.gz"
# Extract the archive
tar -xzf "data/en.tar.gz"
# Extract files in subdirectories.
find "data/OpenSubtitles2016" -name '*.gz' -exec gunzip '{}' \;