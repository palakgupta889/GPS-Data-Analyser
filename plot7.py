from matplotlib import pyplot as plt
from gpxplotter.gpxread import read_gpx_file
from xml.dom import minidom
from datetime import datetime
from math import atan, atan2, radians, tan, sin, cos, sqrt
import numpy as np
from gpxplotter.mplplotting import plot_map, save_map, plot_map_colour,plot_map_colour_existing
import os
from os import listdir,path
from os.path import isfile, join
import sys
from math import sqrt, floor
from bs4 import BeautifulSoup as Soup
from boundingbox import GeoLocation

########## FEW Initialisations ############ 
arguments = sys.argv[1:]
count = len(arguments)
if( count < 2 ):
    print( "Format as below" )
    print( "python3 plo5.py input_directories/example2 coordinates.txt customOutputName" );
    sys.exit(1);

direc  = arguments[0]
infile = arguments[1]
out    = arguments[2]

# os.system("python -W  test.py")
# sys.exit(0)

outhtml = out + "_map.html";
outlegend = out + "_legend.txt"
outsplit = out + "_split.html"
outsplit2 = out + "_split2.html"

distance = 0.015  ####bounding box distance

fp = open( infile ,"r")

my_path = os.path.abspath(os.path.dirname(__file__))
gpxdir = os.path.join(my_path, direc )
files = [f for f in listdir(gpxdir) if isfile(join(gpxdir, f))]
abs_files  = [ os.path.join(gpxdir , f ) for f in files ] 

# colour = ['r', 'g', 'b','c','k','m','w','y']
colour = ['red', 'green', 'blue','cyan','black','magenta','white','yellow']

fig = plt.figure()
abs_files = sorted(list(abs_files))
count  = 0 


######## Read Total Lines #########
totalLines = 0
with open(infile, 'r') as f:
    for line in f:
        totalLines += 1

segCount = int(totalLines/4) #total number of segments to check

##list for coordinates of segment
latStart = []
lonStart = []
latEnd = []
lonEnd = []

####### Read the coordinates #######
for i in range (0,segCount):
    # print("Enter 1st point latituted")
    latStart.append( float(fp.readline()) )
    # print("Enter 1st point longitude")
    lonStart.append( float(fp.readline()) )
    # print("Enter 2nd point latituted")
    latEnd.append( float(fp.readline()) )
    # print("Enter 2nd point longitude")
    lonEnd.append ( float(fp.readline()) )


#Declare lists for bounding box
latStart_ub = []
latStart_lb = []
lonStart_ub = []
lonStart_lb = []
latEnd_ub = []
latEnd_lb = []
lonEnd_ub = []
lonEnd_lb = []

#calculating bounding box
for i in range (0,segCount):
    # print("****",i)
    locStart = GeoLocation.from_degrees(latStart[i], lonStart[i])
    SW_locStart, NE_locStart = locStart.bounding_locations(distance)
    latStart_ub.append( NE_locStart.deg_lat )
    latStart_lb.append( SW_locStart.deg_lat )
    lonStart_ub.append( NE_locStart.deg_lon )
    lonStart_lb.append( SW_locStart.deg_lon )

    locEnd = GeoLocation.from_degrees(latEnd[i], lonEnd[i])
    SW_locEnd, NE_locEnd = locEnd.bounding_locations(distance)
    latEnd_ub.append( NE_locEnd.deg_lat )
    latEnd_lb.append( SW_locEnd.deg_lat )
    lonEnd_ub.append( NE_locEnd.deg_lon )
    lonEnd_lb.append( SW_locEnd.deg_lon )

# print( len(latStart_lb) , len(latStart_ub) , len(latEnd_lb) , len(latEnd_ub) , len(lonStart_lb) , len(lonStart_ub) , len(lonEnd_lb) , len(lonEnd_ub) )
#finding the segments in rides
rides = []
segmentList = list( )
for i in range(0, segCount):
    rides = list()
    segmentList.append( rides )

for file  in abs_files:
    for track in read_gpx_file(file):
        for k, segment in enumerate(track['segments']):
            lat = segment['lat']
            lon = segment['lon']
            for segInd in range(0, segCount):
                flagStart = 0
                flagEnd = 0
                for i in range ( 0 ,np.size(lat) ):
                    if( lat[i] <= latStart_ub[segInd] and lat[i] >= latStart_lb[segInd] and lon[i] <= lonStart_ub[segInd] and lon[i] >= lonStart_lb[segInd] ):
                        flagStart = 1
                        startInd = i
                        break
                if( flagStart == 0 ):
                    continue
                for j in range ( i , np.size(lat) ):
                    if( lat[j] <= latEnd_ub[segInd] and lat[j] >= latEnd_lb[segInd] and lon[j] <= lonEnd_ub[segInd] and lon[j] >= lonEnd_lb[segInd] ):
                        flagEnd = 1
                        endInd = j
                        break
                if( flagEnd == 0 ):
                    continue

                newTrack = [startInd , endInd , segment, track['name'][0]]
                segmentList[segInd].append( newTrack )


#Calculating the metrics
segmentMetricList = list()

for segInd in range(0, segCount):
    finalList = []
    rides = segmentList[segInd]
    for i , newTrack in enumerate(rides):
        startInd = newTrack[0]
        endInd = newTrack [1]
        data = newTrack[2]
        trackName = newTrack[3]

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

    segmentMetricList.append( finalList )


########## READ GPX ############

for file  in abs_files:
    for track in read_gpx_file(file):
        for i, segment in enumerate(track['segments']):            
            fig = plot_map_colour_existing(track, segment, fig, (count+1)*(111), colour[count%8])
    count += 1

save_map(fig, outhtml)
#file_out.close()



#saving graphs
for segInd, finalList in enumerate(segmentMetricList):
    tracksNames = [ x[0] for x in  finalList ]
    speed = [ x[3] for x in  finalList ]
    time = [ x[2] for x in  finalList ]
    index = np.arange(len(tracksNames))
    # fig = plt.figure()
    plt.bar(index, speed)
    plt.xlabel('Track Names', fontsize=10)
    plt.ylabel('Speed (Km/Hr)', fontsize=10)
    plt.xticks(index, tracksNames, fontsize=5, rotation=30)
    plt.title('Speed for segment ' +str(segInd+1))
    plotName = out + "seg" + str(segInd) + ".png"
    plt.savefig(plotName)




########## Partial GPX Plot done ######

#copying template split html
if path.isfile(outsplit):
    os.system( "rm " + outsplit )


mapName  = "map"+ out + ".js"

if path.isfile(mapName):
    os.system( "rm " + mapName)

os.system( "cp ./template/split.html " + outsplit )

#Get MAP ID
fp = open( outhtml )
for i, line in enumerate(fp):
    if i == 10:
        mapid = line.split("\"")[1]
        break
fp.close()

########## Copying map to half map

os.system("awk 'NR>=13 && NR<=37' " + outhtml + " > " + mapName )
os.system("sed -i 's/map.js/"+mapName+"/g' " + outsplit )
os.system("sed -i 's/newmapvalue/"+mapid+"/g' " + outsplit )

#
#
#Get original rides data


#editing split file for adding our data
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
comhead.append("\n\n" + str(segCount) + " segments were analysed " )

for j, finalList in enumerate(segmentMetricList):

    comdiv.append(soup.new_tag("div", id = "segment" + str(j), style = "padding-top:5px;padding-left:100px;width:1000px; text-align:left; font-size:25px"))
    comdiv.append(soup.new_tag('br'))
    segdiv = soup.find( "div", {"id": "segment" + str(j)} )

    divSeg = "seg" + str(j) + "_"

    segdiv.append(soup.new_tag("h2", id = "heading2" + str(j), style = "padding-top:5px;width:1000px; text-align:left; font-size:25px"))

    h2div = soup.find( "h2", {"id": "heading2" + str(j)} )

    h2div.append( "\n" + "Segment " + str( j + 1 ) + "(Found in " + str(len( finalList )) + " rides):" )
    comdiv.append(soup.new_tag('br'))

    for i, lst in enumerate(finalList):

        segdiv.append(soup.new_tag("div", id = divSeg + "ride" + str(i), style = "padding-top:5px;width:1000px; height:200px; text-align:left; font-size:25px"))
        mydivs.append(soup.new_tag('br'))    
        mydivs = soup.find("div", {"id": divSeg + "ride" + str(i)})

        mydivs.append(str(i+1)+". "+str(lst[0]))

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


    segdiv.append(soup.new_tag("img", src = out + "seg"+str(j)+".png"))

    segdiv.append(soup.new_tag('br'))
    
    segdiv.append(soup.new_tag('br'))


with open(outsplit2, "w") as file:
    file.write(str(soup))


# open custom html only : currently : outsplit
import webbrowser
fullpath = os.getcwd()
newfullpath = os.path.join(fullpath , outsplit2)
webbrowser.open('file://' + newfullpath)

fp.close()