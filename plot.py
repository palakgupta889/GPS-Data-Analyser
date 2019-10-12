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


file1 = 'gps_Data/Evening_ride_08_11.gpx'
file2 = 'test_3seg.gpx'
file3 = 'test_3seg2.gpx'

my_path = os.path.abspath(os.path.dirname(__file__))
gpxdir = os.path.join(my_path, 'input' )
files = [f for f in listdir(gpxdir) if isfile(join(gpxdir, f))]
abs_files  = [ os.path.join(gpxdir , f ) for f in files ] 
print( abs_files ) 

# for tracks in read_gpx_file('/gps_Data/7_10_17_kamand_katindi_mandi_bal_valley.gpx'):
#     print(tracks.keys())
#     for segment in tracks['segments']:
#         print(segment.keys())
#         #print('Average heart rate:', segment['average-hr'])

colour = ['red', 'green', 'blue','yellow','black']
fig = plt.figure()

count  = 0 
for file  in abs_files:
    for track in read_gpx_file(file):
        for i, segment in enumerate(track['segments']):
            fig = plot_map_colour_existing(track, segment, fig, colour[count])
    count += 1

save_map(fig, 'map012.html')






# for track in read_gpx_file(file3):
#     for i, segment in enumerate(track['segments']):
#         fig = plot_map_colour_existing(track, segment, fig, colour[i])

# # for track in read_gpx_file(file3):
# #     for i, segment in enumerate(track['segments']):
# #         if( i == 0 ):
# #             fig = plot_map_colour(track, segment, colour[i])
# #         else:
# #             fig = plot_map_colour_existing(track, segment, fig, colour[i])

# save_map(fig, 'map0.html')

