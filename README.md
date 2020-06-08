# Extract-thumbernail-CFG

## The tool
The tool take as input a binary file and extract from it the Control Flow Graph of each function and store them as images.
By default the image are stored inside a new folder called thumbnail in a png format.
The name of the function concateneted with "\_cfg" is used as name of the picture.
The block are divided in for different group based on the predecessors and successors (is possible to set the color inside the file library.py):
- Green are transition blocks
- Yellow are if block, they present more then one successors
- Red are block without a successor inside the function, they can be either return block or blocks that call another function
- Blue are block with more then one predecessor and at least one of them has bigger addresses than the analyzed block; mainly identifies loop

N.B. If the binary is a position-indipendent executable a warning will pop-up. In this case, based on the type of analyses and the normalization of the graph or not, is possible to obtain different classification result.


## Requirements
Ther required python library can be installed with
```
pip3 install angr-utils
pip3 install bingraphvis
pip3 install Image
pip3 install argparse
```
## How to use

The tool can be called with:
```
Python3 project.py file_name [Options]
```
All available options are:

  -h, --help      show this help message and exit
  -d DSTFOLDER    Folder in which to store the images, the folder is created if does not already exists. By default ./thumbnails folder is used.
  -e              Perform a more accurate analyses of the binary.
  -n              Return a non normalized version of the graph.
  -p              Keep the proportion of the original picture when resizing it.
  -f FORMAT       Format in which store the picture. By default png. Accepted png,jpeg,jpg,gif.
  -s SIZE         Size of the thumbnail in pixels. By default 300.
