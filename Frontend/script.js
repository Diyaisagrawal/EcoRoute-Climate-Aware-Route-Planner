document.addEventListener("DOMContentLoaded", () => {

  /* ================= MAP SETUP ================= */
  const map = L.map("map").setView([20.5937, 78.9629], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(map);

  let userMarker;
  let userCoords = null;
  let currentAQI = null;
  let currentTemp = null;

  /* ================= CURRENT LOCATION ================= */
  function getCurrentLocation() {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        userCoords = [lat, lon];

        map.setView([lat, lon], 14);

        if (userMarker) map.removeLayer(userMarker);

        userMarker = L.marker([lat, lon])
          .addTo(map)
          .bindPopup("📍 You are here")
          .openPopup();

        fetchEnvData(lat, lon);
      },
      () => console.warn("Location permission denied")
    );
  }

  getCurrentLocation();

  /* ================= WEATHER + AQI ================= */
  const weatherKey = "44b5b7e76d0cb12453eceae7b405eb7a";

  async function fetchEnvData(lat, lon) {
    try {
      const weatherRes = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${weatherKey}&units=metric`
      );
      const weatherData = await weatherRes.json();

      currentTemp = weatherData.main.temp;
      document.getElementById("temp").innerText = currentTemp;
      document.getElementById("locationName").innerText = weatherData.name;

      const airRes = await fetch(
        `https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${weatherKey}`
      );
      const airData = await airRes.json();

      currentAQI = airData.list[0].main.aqi;
      const aqiText = ["Good", "Fair", "Moderate", "Poor", "Very Poor"];

      document.getElementById("aqi").innerText =
        `${currentAQI} (${aqiText[currentAQI - 1]})`;

    } catch (err) {
      console.error("Env data error:", err);
    }
  }

  /* ================= OFFLINE AUTOCOMPLETE ================= */
  function setupOfflineAutocomplete(inputId, listId) {
    const input = document.getElementById(inputId);
    const list = document.getElementById(listId);

    input.addEventListener("input", async () => {
      const value = input.value.trim();
      list.innerHTML = "";

      // Fixed option: Current Location
      const currentOption = document.createElement("option");
      currentOption.value = "📍 Current Location";
      list.appendChild(currentOption);

      if (value.length < 2) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:5000/search?q=${encodeURIComponent(value)}&lat=${userCoords[0]}&lon=${userCoords[1]}`
        );

        const places = await res.json();

        places.forEach(name => {
          const option = document.createElement("option");
          option.value = name;
          list.appendChild(option);
        });
      } catch (err) {
        console.error("Search error:", err);
      }
    });
  }

  setupOfflineAutocomplete("from", "fromSuggestions");
  setupOfflineAutocomplete("to", "toSuggestions");

  /* ================= RESOLVE INPUT TO COORDS ================= */
  async function resolveCoordinates(value) {

    // Case 1: Current Location selected
    if (value === "📍 Current Location") {
      if (!userCoords) throw new Error("Current location unavailable");
      return userCoords;
    }

    // Case 2: Offline place selected
    const res = await fetch(
      `http://127.0.0.1:5000/place-coords?name=${encodeURIComponent(value)}`
    );
    const data = await res.json();

    if (data.error) throw new Error("Place not found");

    return [data.lat, data.lon];
  }

  /* ================= ROUTE FORM ================= */
  document.getElementById("routeForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fromValue = document.getElementById("from").value.trim();
    const toValue = document.getElementById("to").value.trim();

    if (!fromValue || !toValue) {
      alert("Please select both From and To");
      return;
    }

    try {
      const startCoords = await resolveCoordinates(fromValue);
      const endCoords = await resolveCoordinates(toValue);

      localStorage.setItem("start", JSON.stringify(startCoords));
      localStorage.setItem("end", JSON.stringify(endCoords));
      localStorage.setItem("aqi", currentAQI ?? 80);
      localStorage.setItem("temp", currentTemp ?? 30);

      window.location.href = "route.html";

    } catch (err) {
      alert(err.message);
    }
  });

});
