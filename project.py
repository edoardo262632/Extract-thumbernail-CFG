from angrutils import *
from PIL import Image
from argparse import *
import sys
import os
import library

def analyze(b, folder, emulate,normalize,proportioned,max_size,format):

    #Perform the analyses to create the CFG
    if not(emulate):
        # Perform a more aproximate analyses
        # based on light-weigth analyses and heuristics method
        cfg = b.analyses.CFGFast(normalize=normalize)
    else:
        # Perform a more accurate analyses based on a simulated analyses
        cfg = b.analyses.CFGEmulated(keep_state=True, normalize=normalize, context_sensitivity_level=0)


    # Iterate over all the functions discovered during the analises
    # Extract the controlflow graph for each functions
    # Create the picture in the desired format and then resize it
    set_plot_style('thick')
    for addr,func in b.kb.functions.items():
        #dot = Digraph(comment='The Round Table' ,graph_attr=cfg.graph)
        #dot.render('test-output/round-table.gv', view=True)
        library.plot_cfg(cfg, "%s/%s_cfg" % (folder, func.name),format = format, func_addr={addr:True})
        img = Image.open("%s/%s_cfg.%s" % (folder, func.name,format))
        if proportioned:
            # Resize the picture keeping the proportion
            # The provided size is the max so first control the longest side
            if img.size[0] > img.size[1]:
                lbase = max_size
                wpercent = (max_size/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
            else:
                hsize = max_size
                wpercent = (max_size/float(img.size[1]))
                lbase = int((float(img.size[0])*float(wpercent)))
            img = img.resize((lbase,hsize), Image.ANTIALIAS)
        else:
            #Create a square image from the original one without considering original proportion
            img = img.resize((max_size,max_size), Image.ANTIALIAS)
        img.save("%s/%s_cfg.%s" % (folder, func.name,format))





usage = "Python3 " + sys.argv[0] + " input_file [options]\nUse the option -h or --help for a more detailed explaination"
parser = ArgumentParser(usage=usage)

parser.add_argument("file_name",
                    help="binary that has to be analyzed")

parser.add_argument('-d', dest='dstFolder', default="./thumbnails",
                help='Folder in which to store the images, the folder is created if does not already exists. By default thumbnails folder is used.')

# Arguments concerning analyses
parser.add_argument("-e", dest="emulate", default=False,
                    action='store_const', const=True,
                    help="Perform a more accurate analyses of the binary.")
parser.add_argument("-n", dest="normalize",default=True,
                    action='store_const', const=False,
                    help="Return a non normalized version of the graph.")

# Arguments concerning Image format
parser.add_argument("-p", dest="proportioned", default=False,
                    action='store_const', const=True,
                help="Keep the proportion of the original picture when resizing it. By default False.")
parser.add_argument("-f", dest="format", default="png",
                help="Format in which store the picture. By default png. Accepted png,jpeg,jpg,gif.")
parser.add_argument("-s", dest="size",type=int,default=300,
                help="Size of the thumbnail in pixels. By default 300")

# Check that the essential arguments are provided
args = parser.parse_args()


os.system('mkdir -p %s' % args.dstFolder)

proj = angr.Project(args.file_name, load_options={'auto_load_libs':False})
analyze(proj,folder=args.dstFolder,emulate=args.emulate,normalize=args.normalize,proportioned=args.proportioned,max_size=args.size,format=args.format)
