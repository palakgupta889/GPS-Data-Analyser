from gpxplotter.gpxread import read_gpx_file
from xml.dom import minidom
from datetime import datetime
from math import atan, atan2, radians, tan, sin, cos, sqrt
import numpy as np
from gpxplotter.mplplotting import plot_map, save_map

for tracks in read_gpx_file('7_10_17_kamand_katindi_mandi_bal_valley.gpx'):
    print(tracks.keys())
    for segment in tracks['segments']:
        print(segment.keys())
        #print('Average heart rate:', segment['average-hr'])

for track in read_gpx_file('7_10_17_kamand_katindi_mandi_bal_valley.gpx'):
    for i, segment in enumerate(track['segments']):
        fig = plot_map(track, segment, zcolor='ele')
        save_map(fig, 'map-{}.html'.format(i))