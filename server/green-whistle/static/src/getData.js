// import { map } from './mapSetup'

// const db = require('../../db.json');

async function askForGeoJSON() {
    let treeJsonData = [];
    // delete IP
    const mapBounds = map.getBounds();
    const southWestLat = mapBounds.getSouthWest().lat;
    const southWestLng = mapBounds.getSouthWest().lng;
    const northEastLat = mapBounds.getNorthEast().lat;
    const northEastLng = mapBounds.getNorthEast().lng;
    const bb = southWestLat.toString() + "," + southWestLng.toString() + ","
        + northEastLat.toString() + "," + northEastLng.toString();
    console.log(bb);
    await $.get("http://10.144.3.210:5000/trees.json",
        {bb: bb},
        function (jsonData) {
            treeJsonData = jsonData;
            console.log(jsonData, "jsonDATA");
        })
        .fail(function () {
            console.log("ERROR OCCURED")
        });
    addMarkersToMap(treeJsonData)
}

function addMarkersToMap(treeJsonData) {
    let trees = [];
    map.eachLayer(function (layer) {
       if (layer._leaflet_id !== 26){
           map.removeLayer(layer);
       }
    });
    treeJsonData.forEach(treeJson => {
        const point = L.geoJson(treeJson, {
            style: function (feature) {
                return feature.properties && feature.properties.style;
            },
            onEachFeature: onEachFeature,
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 8,
                    fillColor: "#ff7800",
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            }
        });
        trees.push(point);
    });
    const treesLayer = L.layerGroup(trees);
    treesLayer.addTo(map);
}

function onEachFeature(feature, layer) {
    // content for each popup on map
    let popupContent = "<p></p>";

    // addition of style to popup content
    if (feature.properties && feature.properties.name) {
        popupContent += feature.properties.name;
    }
    // adding popup to marker
    layer.bindPopup(popupContent);
}