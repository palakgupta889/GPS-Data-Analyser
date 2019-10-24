var map = L.map('map3034e472a0244328ab8b7ead83e02dcc');
L.tileLayer(
  "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  {maxZoom:19, attribution: '<a href="https://github.com/jwass/mplleaflet">mplleaflet</a> | Map data (c) <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'}).addTo(map);

if (gjData.features.length != 0) {
  var gj = L.geoJson(gjData, {
    style: function (feature) {
      return feature.properties;
    },
    pointToLayer: function (feature, latlng) {
      var icon = L.divIcon({'html': feature.properties.html, 
        iconAnchor: [feature.properties.anchor_x, 
                     feature.properties.anchor_y], 
          className: 'empty'});  // What can I do about empty?
      return L.marker(latlng, {icon: icon});
    }
  });
  gj.addTo(map);
  
  map.fitBounds(gj.getBounds());
} else {
  map.setView([0, 0], 1);
}