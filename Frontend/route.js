document.addEventListener("DOMContentLoaded", async () => {

  const map = L.map("map").setView([20.5937, 78.9629], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(map);

  // ================= LOAD FROM STORAGE =================
  const start = JSON.parse(localStorage.getItem("start"));
  const end = JSON.parse(localStorage.getItem("end"));
  const aqi = Number(localStorage.getItem("aqi"));
  const temp = Number(localStorage.getItem("temp"));

  if (!start || !end) {
    alert("Missing route data");
    return;
  }

  // ================= CALL BACKEND =================
  const res = await fetch("http://127.0.0.1:5000/eco-route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      start: start,
      end: end,
      aqi: aqi,
      temp: temp
    })
  });

  const data = await res.json();
  console.log("ROUTE RESPONSE:", data);

  if (!data.features) {
    alert("Route calculation failed");
    return;
  }

  // ================= DRAW ROUTES =================
  const routeLayer = L.geoJSON(
    {
      type: "FeatureCollection",
      features: data.features
    },
    {
      style: feature => ({
        color: feature.properties.color,
        weight: 5
      })
    }
  ).addTo(map);

  map.fitBounds(routeLayer.getBounds());

  // ================= MARKERS =================
  L.marker(start).addTo(map).bindPopup("Start");
  L.marker(end).addTo(map).bindPopup("Destination");

  // ================= SUMMARY =================
  if (data.summary) {
    document.getElementById("routeInfo").innerHTML = `
      <b>Shortest Distance:</b> ${data.summary.shortest_km} km<br>
      <b>Eco Route Distance:</b> ${data.summary.eco_km} km<br>
      <b>Eco Score:</b> ${data.summary.eco_score}
    `;
  } else {
    document.getElementById("routeInfo").innerText =
      "Route summary unavailable";
  }

});
