//Create the map object

var myMap = L.map("map", {
    center : [34.89, 3.87], 
    zoom: 2
} ); 

// myMap.on("zoomend", function(e) {
//     console.log( myMap.getZoom() );
//     console.log( myMap.getCenter() );
// });

// myMap.on("moveend", function(e) {
//     console.log( myMap.getCenter() );
//     console.log( myMap.getZoom() );
// });

//Add our tile Layer
var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
});

//Get our data
var link = "static/data/countries.geojson";

//Helper Function to assign borough color
function colorSelect ( borough ) {
    switch(borough) {
        case "Brooklyn":      return "yellow";
        case "Bronx" :        return "red";
        case "Manhattan":     return "orange";
        case "Staten Island": return "purple";
        case "Queens" :       return "green";
        default: "black";
      }
}
// //Add our styling
// var mapStyle = {
//     color: "white",
//     fillColor: "pink",
//     fillOpacity: .5 ,
//     weight: 1.5
// };

//Plot our data
d3.json(link).then( function(data) {
    L.geoJson(data,
              {style: function(feature) { 
                      return { color: "white", 
                               fillColor: colorSelect(feature.properties.ADMIN),
                               fillOpacity: .5,
                               weight: 1.5 
                             }
                      },
               onEachFeature: function (feature, layer) {
                 layer.on({
                     mouseover: function(event){
                         layer = event.target;
                         layer.setStyle({
                             fillOpacity: 0.9
                         });
                     }, 
                     mouseout: function(event){
                          layer = event.target;
                          layer.setStyle({
                              fillOpacity: 0.5
                          });
                     },
                     click: function(event) {
                         myMap.fitBounds( event.target.getBounds() );
                     }
                 });
                 layer.bindPopup(`<h1>${feature.properties.ADMIN}</h1>`)
                }
            }).addTo(myMap);
});