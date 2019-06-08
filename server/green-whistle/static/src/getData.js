function askForGeoJSON(){
    $.get("http://10.144.3.210:5000/trees.json",
        {bb: "52.205324323965435,20.97427896707837,52.21105683036724,20.98185675745256"},
        function (data) {
            console.log(data);
        })
        .fail(function () {
            console.log("ERROR OCCURED")
        });
}

// askForGeoJSON = () => {
//     $.get("http://10.144.3.210:5000/trees.json",
//         {bb: "52.205324323965435,20.97427896707837,52.21105683036724,20.98185675745256"},
//         function (data) {
//             console.log(data);
//         })
//         .fail(function () {
//             console.log("ERROR OCCURED")
//         });
// }
