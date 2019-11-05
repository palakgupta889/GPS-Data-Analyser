# GPS-Data-Analyser

This is a software which uses GPS data from a gpx file, plots it on an interactive map and analyses it for various metrics relating to fitness activities like running and biking such as speed, elevation gain, performance progress etc.

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
pip install bs4
```

## Running the tests

The gps_Data and input directories contain sample input gpx files that contain GPS Data.

plot5.py contains the script to plot the gpx data on an interactive map on left of the HTML page and statistics for all the plotted rides on the right side along with the common segment statistics whose coordinates are given by the user through a file.
```
python3 plot5.py <path to input directory> <path to coordinates file for common segment> <path to output file>
```

After running the above command, an html file containing the output map and all the statistics will automatically open in your web browser. 

## Authors

* **Nikhil Gupta** - [ngupta26](https://github.com/ngupta26)
* **Palak Gupta** - [palakgupta889](https://github.com/palakgupta889)
* **Anirudh Nistala** - [ssnap03](https://github.com/ssnap03)
