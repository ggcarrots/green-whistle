// map creation
let map = L.map('map').setView([52.20933320698831, 20.974724907134092], 16);

// adding layers to map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.light'
}).addTo(map);

// module.exports = map


// let baseballIcon = L.icon({
//     iconUrl: 'baseball-marker.png',
//     iconSize: [32, 37],
//     iconAnchor: [16, 37],
//     popupAnchor: [0, -28]
// });
//
// function onEachFeature(feature, layer) {
//     // content for each popup on map
//     let popupContent = "<p>I started out as a GeoJSON " +
//         feature.geometry.type + ", but now I'm a Leaflet vector!</p>";
//
//     // addition of style to popup content
//     if (feature.properties && feature.properties.popupContent) {
//         popupContent += feature.properties.popupContent;
//     }
//     // adding popup to marker
//     layer.bindPopup(popupContent);
// }
//
// // loading the bicycleRental and campus from sample-geojson
// L.geoJson([bicycleRental, campus], {
//     style: function (feature) {
//         return feature.properties && feature.properties.style;
//     },
//
//     onEachFeature: onEachFeature,
//     pointToLayer: function (feature, latlng) {
//         return L.circleMarker(latlng, {
//             radius: 8,
//             fillColor: "#ff7800",
//             color: "#000",
//             weight: 1,
//             opacity: 1,
//             fillOpacity: 0.8
//         });
//     }
// }).addTo(map);
//
//
// L.geoJson(freeBus, {
//     filter: function (feature, layer) {
//         if (feature.properties) {
//             // If the property "underConstruction" exists and is true, return false (don't render features under construction)
//             return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
//         }
//         return false;
//     },
//     onEachFeature: onEachFeature
// }).addTo(map);
//
//
// var coorsLayer = L.geoJson(coorsField, {
//     pointToLayer: function (feature, latlng) {
//         return L.marker(latlng, {icon: baseballIcon});
//     },
//     onEachFeature: onEachFeature
//     }).addTo(map);
//
//
