$(document).ready(function () {
  $("#datepicker-container .input-daterange").datepicker({
    todayHighlight: true,
    autoclose: true,
  })

  const coordinates = {
    paris: [2.352222, 48.856613],
    "new york": [-74.006, 40.7128],
    sydney: [151.2093, -33.8688],
    "cape town": [18.4241, -33.9249],
    tokyo: [139.7525, 35.6852],
  }
  const searchCity = $("#search-city")["0"].innerText.toLowerCase()

  mapboxgl.accessToken =
    "pk.eyJ1IjoidHV2bzExMDYiLCJhIjoiY2swYmwwY2IzMHZjbDNucjd1NHl3c3l5OSJ9.oUI6fhdDOx5rzmYV5dGjjg"
  var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: coordinates[searchCity],
    zoom: 12,
  })
})
