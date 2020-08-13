// Load the Visualization API and the columnchart package.
// @ts-ignore TODO(jpoehnelt)
// google.load("visualization", "1", { packages: ["columnchart"] });
google.charts.load("current", {packages:['corechart']});
var lines = []
function initMap() {
  // The following path marks a path
  const path = [
    {
      lat: 22.928099,
      lng: 121.101644
    },
    {
      lat: 22.755720,
      lng: 121.143208
    }
  ];
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: path[1],
    mapTypeId: "terrain"
  });
  // Create an ElevationService.
  const elevator = new google.maps.ElevationService();
  // Draw the path, using the Visualization API and the Elevation service.
  // displayPathElevation(path, elevator, map);
  document.querySelector("#btn_generate").onclick = () =>{
    let lat_a = parseFloat(document.querySelector("#lat_a").value)
    let lng_a = parseFloat(document.querySelector("#lng_a").value)
    let lat_b = parseFloat(document.querySelector("#lat_b").value)
    let lng_b = parseFloat(document.querySelector("#lng_b").value)
    if (isNaN(lat_a)||isNaN(lng_a)||isNaN(lat_b)||isNaN(lng_b)){
      alert("請輸入經緯度")
    }
    else{
      const newpath = [{lat: lat_a,lng: lng_a}, {lat: lat_b,lng: lng_b}]
      // document.querySelector("#elevation_chart").innerHTML = ""
      displayPathElevation(newpath, elevator, map);
    }
  }
}

function displayPathElevation(path, elevator, map) {
  //clear origin lines
  for (i=0; i<lines.length; i++)
{
  lines[i].setMap(null); //or line[i].setVisible(false);
}
  // Display a polyline of the elevation path.
  polyline = new google.maps.Polyline({
    path: path,
    strokeColor: "#0000CC",
    strokeOpacity: 0.4,
    map: map
  });

  lines.push(polyline)
  // Create a PathElevationRequest object using this array.
  // Ask for 256 samples along that path.
  // Initiate the path request.
  elevator.getElevationAlongPath(
    {
      // @ts-ignore TODO(jpoehnelt) update typings to support LatLngLiteral
      path: path,
      samples: 256
    },
    plotElevation
  );
}

// Takes an array of ElevationResult objects, draws the path on the map
// and plots the elevation profile on a Visualization API ColumnChart.
function plotElevation(elevations, status) {
  const chartDiv = document.getElementById("elevation_chart");
  let h1 = parseFloat(document.querySelector("#height_a").value)
  let h2 = parseFloat(document.querySelector("#height_b").value)

  let height_a = isNaN(h1)?  0:h1
  console.log(isNaN(h1))
  let height_b = isNaN(h2)? 0:h2
  console.log(height_a, height_b)
  if (status !== "OK") {
    // Show the error code inside the chartDiv.
    chartDiv.innerHTML =
      "Cannot show elevation: request failed because " + status;
    return;
  }
  // Create a new chart in the elevation_chart DIV.
  const chart = new google.visualization.ColumnChart(chartDiv);
  // Extract the data from which to populate the chart.
  // Because the samples are equidistant, the 'Sample'
  // column here does double duty as distance along the
  // X axis.
  const data = new google.visualization.DataTable();
  data.addColumn("number", "Sample");
  data.addColumn("number", "Elevation");
  data.addColumn("number", "Line");

  for (let i = 0; i < elevations.length; i++) {
    if (i === 0 || i ===(elevations.length-1)){
      if (i === 0){
        data.addRow([i,null, elevations[i].elevation+height_a]);
      }
      else{
        data.addRow([i,null, elevations[i].elevation+height_b]);
      }
      console.log(i)
    }
    else{
      // console.log(i)
      data.addRow([i, elevations[i].elevation,null]);
    }
  }
  google.visualization.events.addListener(chart, 'ready', function () {
        chartDiv.innerHTML = '<img src="' + chart.getImageURI() + '">';
        // console.log(chartDiv.innerHTML);
      });
  const d = haversine_distance(elevations[0].location,elevations[255].location)
  console.log(elevations[0].location.lat())
  // Draw the chart using the data within its DIV.
  chart.draw(data, {
    hAxis: {title: "distance(km): ".concat(d)},
    color:'blue',
    height: 150,
    legend: "none",
    trendlines: { 1:{
    degree: 3,color:'red',
  }},
    // @ts-ignore TODO(jpoehnelt) check versions
    titleY: "Elevation (m)"
  });
}

//cauculate straight line distance
  function haversine_distance(mk1, mk2) {
    console.log("counting distance")
      var R = 6371.0710; // Radius of the Earth in kilometers
      var rlat1 = mk1.lat() * (Math.PI/180); // Convert degrees to radians
      var rlat2 = mk2.lat() * (Math.PI/180); // Convert degrees to radians
      var difflat = rlat2-rlat1; // Radian difference (latitudes)
      var difflon = (mk2.lng()-mk1.lng()) * (Math.PI/180); // Radian difference (longitudes)

      var d = 2 * R * Math.asin(Math.sqrt(Math.sin(difflat/2)*Math.sin(difflat/2)+Math.cos(rlat1)*Math.cos(rlat2)*Math.sin(difflon/2)*Math.sin(difflon/2)));
      return d;
    }
