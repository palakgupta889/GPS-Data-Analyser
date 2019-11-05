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
from boundingbox import GeoLocation

########## FEW CONSTANTS ############ 
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
outsplit2 = out + "_split2.html"
# out = "map.html"
infile = "coordinates.txt"
fp = open( infile ,"r")


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


########## READ GPX ############

for file  in abs_files:
    for track in read_gpx_file(file):
        for i, segment in enumerate(track['segments']):            
            fig = plot_map_colour_existing(track, segment, fig, (count+1)*(111), colour[count%8])
    count += 1

save_map(fig, outhtml)
#file_out.close()


# lat="31.7620270" lon="76.9888490
# 31.7595160" lon="77.0000430

# print("Enter 1st point latituted")
lat1 = float(fp.readline())
# print("Enter 1st point longitude")
lon1 = float(fp.readline())
# print("Enter 2nd point latituted")
lat2 = float(fp.readline())
# print("Enter 2nd point longitude")
lon2 = float(fp.readline())

loc1 = GeoLocation.from_degrees(lat1, lon1)
distance = 0.005  # 1 kilometer
SW_loc1, NE_loc1 = loc1.bounding_locations(distance)

lat1_ub = NE_loc1.deg_lat
lat1_lb = SW_loc1.deg_lat
lon1_ub = NE_loc1.deg_lon
lon1_lb = SW_loc1.deg_lon

loc2 = GeoLocation.from_degrees(lat2, lon2)
distance = 0.01  # 1 kilometer
SW_loc2, NE_loc2 = loc2.bounding_locations(distance)

lat2_ub = NE_loc2.deg_lat
lat2_lb = SW_loc2.deg_lat
lon2_ub = NE_loc2.deg_lon
lon2_lb = SW_loc2.deg_lon


# print( NE_loc )
# print( SW_loc )

# print( lat1_ub , lon1_ub , lat1_lb , lon1_lb )
# print( lat2_ub , lon2_ub , lat2_lb , lon2_lb )

rides = []

for file  in abs_files:
    for track in read_gpx_file(file):
        for k, segment in enumerate(track['segments']):
            # print( "in for loop" )
            lat = segment['lat']
            lon = segment['lon']
            flagStart = 0
            flagEnd = 0
            # for i in range ( 0 ,np.size(lat) ):
            #     print(lat[i] , lon[i])
            #     if( lat[i] == lat1 and lon[i] == lon1):
            #         print("helll yeah")
            for i in range ( 0 ,np.size(lat) ):
                if( lat[i] <= lat1_ub and lat[i] >= lat1_lb and lon[i] <= lon1_ub and lon[i] >= lon1_lb ):
                    flagStart = 1
                    startInd = i
                    # print("start found")
                    break
            if( flagStart == 0 ):
                continue
            for j in range (i,np.size(lat)):
                if( lat[j] <= lat2_ub and lat[j] >= lat2_lb and lon[j] <= lon2_ub and lon[j] >= lon2_lb ):
                    flagEnd = 1
                    endInd = j
                    break
            if( flagEnd == 0 ):
                continue

            newTrack = [startInd , endInd , segment, track['name'][0]]
            rides.append( newTrack )

#print( "\n\ncommon segment found in " , len(rides) , " rides" )

finalList = []

for i , newTrack in enumerate(rides):
    startInd = newTrack[0]
    endInd = newTrack [1]
    trackName = newTrack[3]
    data = newTrack[2]

    distance = data['distance'][endInd] - data['distance'][startInd]
    distance = round(distance / 1000,3)
    time = data['delta-seconds'][endInd] - data['delta-seconds'][startInd]
    # time = round(time / 3600,3)
    speed = round(distance*3600/time,3)

    elevation = data['ele'][startInd:endInd+1]
    # print( len(elevation) )
    ele_diff = np.diff(elevation)
    eleup = round(ele_diff[np.where(ele_diff > 0)[0]].sum(),3)
    eledown = round(ele_diff[np.where(ele_diff < 0)[0]].sum(),3)

    #print("\n\n", i+1,". ", trackName)
    #print( "dist = ", distance , " km" )
    #print( "time = ",  int(time/3600), ":" , int((time%3600)/60) , ":" , int(time%60) )
    #print( "speed = ", speed, " km/hr" )
    #print( "eleup = ", eleup , " m" )
    #print( "eledown = ", -eledown , " m")
    # print(distance, time, speed , eleup , eledown)
    # print( trackName )

    lst = [trackName , distance , time , speed, eleup , eledown ]

    finalList.append(lst)


os.system( "rm " + outsplit )
os.system( "rm map.js ")
os.system( "cp ./template/split.html " + outsplit )

fp = open( outhtml )
for i, line in enumerate(fp):
    if i == 10:
        mapid = line.split("\"")[1]
        break
fp.close()

#segment calculation done

########## Copying map to half map

os.system("awk 'NR>=13 && NR<=37' " + outhtml + " > map.js" )
os.system("sed -i 's/newmapvalue/"+mapid+"/g' " + outsplit )

#### original rides data

soup = Soup(open(outsplit), "html.parser")

maindiv = soup.find("div", {"id": "legend"})
tot = count - 1
count = 0

for file  in abs_files:
	for track in read_gpx_file(file):
		for i, segment in enumerate(track['segments']):
			
			maindiv.append(soup.new_tag("div", id = "new_ride" + str(count), style = "padding-top:5px;padding-left:100px;width:1000px; height:250px; text-align:left; font-size:25px"))				
			
			mydivs = soup.find("div", {"id": "new_ride" + str(count)})
			
			total_uphill = round(segment['ele-up'],2)
			total_downhill = round(segment['ele-down'],2)
			total_distance = round(segment['distance'][-1]/1000,2)
			time = segment['delta-seconds'][-1]
			total_time_seconds = round(segment['delta-seconds'][-1]/3600,2)
			speed = round(total_distance/total_time_seconds,2)

			mydivs.append(soup.new_tag("button", style = "height: 40px; width: 40px; background: " + str(colour[count%8])))
			
			#mydivs.append( str(colour[count%8]) + " --------> " +  str(track['name'][0]))
			mydivs.append( "  "+ str(track['name'][0]))
			mydivs.append(soup.new_tag('br'))
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

comdiv = soup.find("div", {"id": "common-segment"})
comhead = soup.find("h2")
comhead.append("\n\nCommon segment found in " +str(len(rides))+ " rides: ")

for i, lst in enumerate(finalList):

	comdiv.append(soup.new_tag("div", id = "ride" + str(i), style = "padding-top:5px;padding-left:100px;width:1000px; height:250px; text-align:left; font-size:25px"))
	
	mydivs = soup.find("div", {"id": "ride" + str(i)})

	mydivs.append(str(i+1)+". "+str(lst[0]))

	mydivs.append(soup.new_tag('br'))
	mydivs.append(soup.new_tag('br'))

	mydivs.append("Distance = "+str(lst[1])+" Km")

	mydivs.append(soup.new_tag('br'))

	mydivs.append("Time = " + str(int(lst[2]/3600))+ ":" + str(int(lst[2]%3600/60)) + ":" + str(int(lst[2]%60)))

	mydivs.append(soup.new_tag('br'))

	mydivs.append("Speed = " + str(lst[3])+" Km/hr")

	mydivs.append(soup.new_tag('br'))

	mydivs.append("Elevation up = " + str(lst[4])+" m")

	mydivs.append(soup.new_tag('br'))

	mydivs.append("Elevation down = " + str(lst[5])+" m")

	mydivs.append(soup.new_tag('br'))
	mydivs.append(soup.new_tag('br'))

with open(outsplit2, "w") as file:
    file.write(str(soup))



# open custom html only : currently : outsplit
import webbrowser
fullpath = os.getcwd()
newfullpath = os.path.join(fullpath , outsplit2)
webbrowser.open('file://' + newfullpath)

fp.close()