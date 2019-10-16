# from gpxplotter import read_gpx_file
# from gpxplotter.mplplotting import plot_elevation_hr_multi_dist, save_fig
# from matplotlib import pyplot as plt
# plt.style.use('seaborn-poster')


# for track in read_gpx_file('test.gpx'):
#   print(track)
#   for i, segment in enumerate(track['segments']):
#     print(i)
#     fig = plot_elevation_hr_multi_dist(track, segment)
#     save_fig(fig, 'test-{}.png'.format(i))


# from gpxplotter import read_gpx_file
# from gpxplotter.mplplotting import plot_map, save_map


# for track in read_gpx_file('test.gpx'):
#     for i, segment in enumerate(track['segments']):
#         fig = plot_map(track, segment, zcolor='pulse')
#         save_map(fig, 'test-{}.html'.format(i))





from matplotlib import pyplot as plt

from gpxplotter import read_gpx_file
from gpxplotter.mplplotting import plot_map, save_map, plot_map2


fig = plt.figure()
count = 0;
for track in read_gpx_file('test.gpx', maxpulse=187):
  for i, segment in enumerate(track['segments']):
    count += 1
    if( count == 1 ):
      fig = plot_map(track, segment, zcolor='ele')
      save_map(fig, 'map.html'.format(i))
    else:
      fig = plot_map2(track, segment, fig, zcolor='pulse')
      save_map(fig, 'map.html'.format(i))

print(count)

# for track in read_gpx_file('test.gpx', maxpulse=187):
#     for i, segment in enumerate(track['segments']):
#         fig = plot_map(track, segment, zcolor='pulse')
#         save_map(fig, 'map-{}.html'.format(i))