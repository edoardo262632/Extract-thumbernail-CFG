# Extract-thumbernail-CFG

## The tool
The tool take as input a binary file and extract from it the Control Flow Graph of each function and store them as images.
By default the image are stored inside a new folder called thumbnail in a png format. 
The name of the function concateneted with "\_cfg" is used as name of the picture.


## How to use



Options:

  -h, --help    show this help message and exit
  -d DSTFOLDER  Folder in which to store the images, the folder is created if does not already exists. By default thumbnails
                folder is used.
  -e            Perform a more accurate analyses of the binary. By default False.
  -n            Return a normalized version of the graph. By default True.
  -p            Keep the proportion of the original picture when resizing it. By default False.
  -f FORMAT     Format in which store the picture. By default png. Accepted png,jpeg,jpg,gif.
  -s SIZE       Size of the thumbnail in pixels. By default 300
