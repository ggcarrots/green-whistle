map.on("moveend", async function () {
    askForGeoJSON();
});

map.on("load", async function () {
    askForGeoJSON();
});

map.on("resize", async function () {
    askForGeoJSON();
});

function updateSidebar(feature) {
    if (feature.properties){
        $( "#species" ).html(feature.properties.species);
        $( "#inventory_number" ).html(feature.properties.inventory_number);
        $( "#status" ).html(feature.properties.status);
        $( "#management_unit" ).html(feature.properties.management_unit);
        $( "#updated" ).html(feature.properties.updated);
        $( "#cut_out_reason" ).html(feature.properties.cut_out_reason);
    }
}