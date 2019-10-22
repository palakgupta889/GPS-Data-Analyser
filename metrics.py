import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go
#import haversine
import os
from os import listdir
from os.path import isfile, join
import sys

arguments = sys.argv[1:]
count = len(arguments)
# print( count  )
'''
if( count < 2 ):
	print( "Format as below" )
	print( "python3 file directory mapname" );
	sys.exit(1);
'''

direc = arguments[0]

my_path = os.path.abspath(os.path.dirname(__file__))
gpxdir = os.path.join(my_path, direc )
files = [f for f in listdir(gpxdir) if isfile(join(gpxdir, f))]
abs_files  = [ os.path.join(gpxdir , f ) for f in files ] 

abs_files = sorted(list(abs_files))
count  = 0 
for file  in abs_files:
	gpx_file = open(file, 'r')
	gpx = gpxpy.parse(gpx_file)
	print (len(gpx.tracks))
	print (len(gpx.tracks[0].segments))
	print (len(gpx.tracks[0].segments[0].points))
	data = gpx.tracks[0].segments[0].points
	df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
	for point in data:
		df = df.append({'lon': point.longitude, 'lat': point.latitude, 'alt': point.elevation, 'time': point.time}, ignore_index=True)
	print (df.head())