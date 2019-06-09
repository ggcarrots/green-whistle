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
        if (feature.properties.status === "request"){
            $( "#status_big_div" ).css({'background-color': '#ff3333'})
        }
        else{
            $( ".detail:nth-child(odd)" ).css({'background-color': '#009933b2'})
        }
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

// $( '.map').click(function (event) {
//     event.stopPropagation();
//     $( ".sidebar" ).css({'opacity': '0'});
// });