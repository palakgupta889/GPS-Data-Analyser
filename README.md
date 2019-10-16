# GPS-Data-Analyser

This is a software which uses GPS data from a gpx file, plots it on an interactive map and analyses it for various metrics realting to fitness activities like running and biking such as speed, elevation gain, performance progress etc.

## Getting Started

Clone this git repository using the following command:
```
git clone https://github.com/palakgupta889/GPS-Data-Analyser.git
```

### Pre-requisites

Python 3.0 or above

Install the following python packages:
```
pip install mplleaflet
pip install numpy
pip install matplotlib
```

## Running the tests

The gps_Data and input directories contain sample input gpx files that contain GPS Data.

plot2.py contains the script to plot the gpx data on an interactive map.
```
python3 plot2.py directory mapname
```
where directory is the input directory name and mapname is the name of the output map.

After running the above command, an html file containing the output map will automatically open in your web browser. A text file containing the legend for the map, regarding which color indicates which trip, is also created. 

## Authors

* **Nikhil Gupta** - [ngupta26](https://github.com/ngupta26)
* **Palak Gupta** - [palakgupta889](https://github.com/palakgupta889)
* **Anirudh Nistala** - [ssnap03](https://github.com/ssnap03)
