map.on("moveend", async function () {
    askForGeoJSON();
});

map.on("load", async function () {
    askForGeoJSON();
});

map.on("resize", async function () {
    askForGeoJSON();
});