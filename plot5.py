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
from math import sqrt, floor

from bs4 import BeautifulSoup as Soup

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

outsplit = out + "_split.html"
# out = "map.html"

#file_out = open( outlegend ,"w")

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
            #total_uphill = round(segment['ele-up'],2)
            #total_downhill = round(segment['ele-down'],2)
            #total_distance = round(segment['distance'][-1]/1000,2)
            #time = segment['delta-seconds'][-1]
            #total_time_seconds = round(segment['delta-seconds'][-1]/3600,2)
            #print('Total Time : ', floor(segment['delta-seconds'][-1]/60),' min ', int(segment['delta-seconds'][-1]%60),' sec ')
            #speed = round(total_distance/total_time_seconds,2)
            
            fig = plot_map_colour_existing(track, segment, fig, (count+1)*(111), colour[count%8])
            # print( colour[count%8] , " --------> ", track['name'][0] )
            #file_out.write( str(colour[count%8]) + " --------> " +  str(track['name'][0])  + "\n")
            #file_out.write( "Stats: "+ "\n")
            #file_out.write( "Total uphill : " + str(total_uphill) + " m"  + "\n")
            #file_out.write( "Total downhill : " + str(total_downhill) + " m"  + "\n")
            #file_out.write( "Total distance : " + str(total_distance) + " Km"  + "\n")
            #file_out.write( "Total time : " + str(floor(time/3600))+ ":" + str(floor((time%3600)/60)) + ":" + str(int(time%60)) + "\n")
            #file_out.write( "Speed : " + str(speed) + " Km/hr"  + "\n\n\n")
            # print( file.split('/')[-1] , " ---- ",   colour[count%8] , " --------> ", track['name'][0] )
    count += 1

save_map(fig, outhtml)
#file_out.close()



os.system( "rm " + outsplit )
os.system( "rm map.js ")
os.system( "cp ./template/split.html " + outsplit )

fp = open( outhtml )
for i, line in enumerate(fp):
    if i == 10:
        mapid = line.split("\"")[1]
        break
fp.close()

os.system("awk 'NR>=13 && NR<=37' " + outhtml + " > map.js" )
os.system("sed -i 's/newmapvalue/"+mapid+"/g' " + outsplit )

soup = Soup(open(outsplit), "html.parser")

maindiv = soup.find("div", {"id": "legend"})

count = 0

for file  in abs_files:
	for track in read_gpx_file(file):
		for i, segment in enumerate(track['segments']):
			maindiv.append(soup.new_tag("div", id = "new_ride" + str(count)))

			mydivs = soup.find("div", {"id": "new_ride" + str(count)})

			total_uphill = round(segment['ele-up'],2)
			total_downhill = round(segment['ele-down'],2)
			total_distance = round(segment['distance'][-1]/1000,2)
			time = segment['delta-seconds'][-1]
			total_time_seconds = round(segment['delta-seconds'][-1]/3600,2)
			speed = round(total_distance/total_time_seconds,2)
			mydivs.append( str(colour[count%8]) + " --------> " +  str(track['name'][0]))
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Stats: ")
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Total uphill : " + str(total_uphill) + " m" )
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Total downhill : " + str(total_downhill) + " m")
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Total distance : " + str(total_distance) + " Km" )
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Total time : " + str(floor(time/3600))+ ":" + str(floor((time%3600)/60)) + ":" + str(int(time%60)) )
			mydivs.append(soup.new_tag('br'))
			mydivs.append( "Speed : " + str(speed) + " Km/hr")
			mydivs.append(soup.new_tag('br'))
			mydivs.append(soup.new_tag('br'))
	count += 1

with open("output1.html", "w") as file:
    file.write(str(soup))