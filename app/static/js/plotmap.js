//Create the map object, only if the "map" div is in the DOM
var myMap = null;
if (document.getElementById("map")) {

  var myMap = L.map("map", {
      center : [34.89, 3.87], 
      zoom: 2
  });
  
  var stripes = new L.StripePattern();
  stripes.addTo(myMap);

}

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




//Helper Function to assign country color
function styleSelect ( country_code ) {
  // console.log("looking for color for country_code_a3 :" + country_code)
    country_obj = country_data.find( o => o.country_code_a3 === country_code);
    if (country_obj) { 
        //console.log("Found country: " + country_obj.country_name);
        pct_satis = country_obj.total > 0 ? (country_obj.satisfactory/country_obj.total) * 100 : 0; 
    }
    else  {
        return { color: "white", 
                 fillColor: "white",
                 fillPattern : stripes,
                 fillOpacity: .5,
                 weight: 1.5 
      }
    }

    if (between(pct_satis, 1,25)) {
        return { color: "white", 
                 fillColor: "red",
                 fillOpacity: 1,
                 weight: 1.5 
               }
    }
    else if (between(pct_satis, 25,50)) { 
        return { color: "white", 
                 fillColor: "red",
                 fillOpacity: .75,
                 weight: 1.5 
               }
    }
    else if (between(pct_satis, 50, 75)) {
        return { color: "white", 
                 fillColor: "red",
                 fillOpacity: .25,
                 weight: 1.5 
               }
    }
    else if (between(pct_satis, 75, 100)) {
        return { color: "white", 
                 fillColor: "red",
                 fillOpacity: .1,
                 weight: 1.5 
               }
    }
    else { //No project data or no information avaialable
        return { color: "white", 
                 fillColor: "rose",
                 fillOpacity: .05,
                 fillPattern : stripes,
                 weight: 1.5 
      }
    }

}

function getTooltipHTML ( country_code ) {
    //console.log("looking for color for country_code_a3 :" + country_code)
     country_obj = country_data.find( o => o.country_code_a3 === country_code);
     if (country_obj) { 
         //console.log("Found country: " + country_obj.country_name);
         pct_satis = country_obj.total > 0 ? (country_obj.satisfactory/country_obj.total) * 100 : 0; 
         pct_satis = Math.round(pct_satis);
         return country_obj.total > 0 ? `<div class="text-center">${country_obj.country_name}</div><hr><p>${pct_satis} % satisfactory</p>` :  
                                        `<div class="text-center">${country_obj.country_name}</div><hr><p>No Project Information</p>`
     }
     else  {
         return "<p>No Information Available</p>"
     }
 }

 function showTable( country_code ) {
     //Shows the project-table class table with data from API
    let url = `/api/v1.0/project/${country_code}`

    console.log("Calling showTable with" + url)

    d3.select(".dataTable-wrapper").remove();
    let table = d3.select(".table-div").append("table").attr("class", "projects-table");
     
    if (!table) {
        return;
    }
    fetch(url)
    .then(response => response.json())
    .then(data => {


      if (!data.length) {
        return
      }

      data.forEach( item => console.log(Object.values(item))); 

      table = new simpleDatatables.DataTable(".projects-table", {
        data: {
          headings: Object.keys(data[0]),
          data: data.map(item => Object.values(item))
        }
      });

    })
 }

function between(x, min, max) {
    return x >= min && x <= max;
}

function hideSpinner() {
  document.getElementById('spinner').style.display = 'none';
} 


//Locations of the data sources
var link = "static/data/countries.geojson";
var stats_url = "/api/v1.0/summary"

//Plot our data
//Each country's color is based on how many satisfactory projects it had.
if (myMap) {
  d3.json(stats_url).then ( function(data) {
    country_data = data;
    d3.json(link).then( function(data) {
        L.geoJson(data,
                {style: function(feature) {
                        styleObj = styleSelect(feature.properties.ISO_A3);
                        //console.log (styleObj);
                        return styleObj;
                      },
                onEachFeature: function (feature, layer) {
                    //console.log(layer);
                  layer.on({
                      mouseover: function(event){
                          layer = event.target;
                          //  layer.setStyle({
                          //      fillOpacity: 0.9
                          //  });
                          this.openPopup();
                      }, 
                      mouseout: function(event){
                            layer = event.target;
                          //   layer.setStyle({
                          //       fillOpacity: 0.5
                          //   });
                            this.closePopup();
                      },
                      click: function(event) {
                          myMap.fitBounds( event.target.getBounds() );
                          showTable(feature.properties.ISO_A3);
                      }
                  });

                  
                
                      layer.bindTooltip(getTooltipHTML(feature.properties.ISO_A3));

                      hideSpinner();

                  }
              }).addTo(myMap);
            
    });


  });
}