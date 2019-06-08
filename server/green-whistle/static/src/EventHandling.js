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
        // if (feature.properties.status === "request"){
        //     $( "#status" ).css({'background-color': '#ff3333b3'})
        // }
        // else{
        //     $( "#status" ).css({'color': '#ffffb3','background-color': '#00ff66b3'})
        // }
        $( "#management_unit" ).html(feature.properties.management_unit);
        $( "#updated" ).html(feature.properties.updated);
        $( "#cut_out_reason" ).html(feature.properties.cut_out_reason);
    }
}

$( '#directives_button').click(function () {
    $( ".directives" ).css({'display': 'inline'});
    $( ".main-body" ).css({'display': 'none'})
});

$( '.logo').click(function () {
    $( ".directives" ).css({'display': 'none'});
    $( ".main-body" ).css({'display': 'inline'})
});