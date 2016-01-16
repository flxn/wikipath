# wikipath
find the shortest path between two wikipedia articles

![alt text](https://raw.githubusercontent.com/flxn/wikipath/master/screenshot.png "wikipath screenshot")


### Parsing a Wikipedia dump
1. Download a Wikipedia database dump from  https://dumps.wikimedia.org/backup-index.html
2. run ```parse.py YOUR_DUMP_FILE``` to parse the dump. The script creates two files ("graph_out.csv" and "nodes.txt") in the current directory.

### Running wikipath
Run wikipath with ```python wikipath.py graph_out.csv nodes.txt```.

### Requirements
- Python2.7
- 8GB RAM
