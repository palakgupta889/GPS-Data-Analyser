from matplotlib import pyplot as plt
from gpxplotter.gpxread import read_gpx_file
from xml.dom import minidom
from datetime import datetime
from math import atan, atan2, radians, tan, sin, cos, sqrt
import numpy as np
from gpxplotter.mplplotting import plot_map, save_map, plot_map_colour,plot_map_colour_existing
import os
from os import listdir
from os.path import isfile, join
import sys
import copy

arguments = sys.argv[1:]
count = len(arguments)
# print( count  )
if( count < 2 ):
	print( "Format as below" )
	print( "python3 file directory mapname" );
	sys.exit(1);


direc = arguments[0]
# direc = "input"
out = arguments[1]
outhtml = out + "_map.html";
outlegend = out + "_legend.txt"
# out = "map.html"

file_out = open( outlegend ,"w")

my_path = os.path.abspath(os.path.dirname(__file__))
gpxdir = os.path.join(my_path, direc )
files = [f for f in listdir(gpxdir) if isfile(join(gpxdir, f))]
abs_files  = [ os.path.join(gpxdir , f ) for f in files ] 

# colour = ['r', 'g', 'b','c','k','m','w','y']
colour = ['red', 'green', 'blue','cyan','black','magenta','white','yellow']

fig = plt.figure()
abs_files = sorted(list(abs_files))
count  = 0 
for file  in abs_files:
    for track in read_gpx_file(file):
        for i, segment in enumerate(track['segments']):
            fig = plot_map_colour_existing(track, segment, fig, (count+1)*(111), colour[count%8])
            # print( colour[count%8] , " --------> ", track['name'][0] )
            file_out.write( str(colour[count%8]) + " --------> " +  str(track['name'][0])  + "\n")
            # print( file.split('/')[-1] , " ---- ",   colour[count%8] , " --------> ", track['name'][0] )
    count += 1

# fig2 = copy.deepcopy(fig);
plt.show(fig)
# save_map(fig, outhtml)
file_out.close()
