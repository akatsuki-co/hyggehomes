$(document).ready(function () {
  $("#datepicker-container .input-daterange").datepicker({
    todayHighlight: true,
    autoclose: true,
  })
  mapboxgl.accessToken =
    "pk.eyJ1IjoidHV2bzExMDYiLCJhIjoiY2swYmwwY2IzMHZjbDNucjd1NHl3c3l5OSJ9.oUI6fhdDOx5rzmYV5dGjjg"
  var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v11",
    center: [2.352222, 48.856613],
    zoom: 9,
  })
})
