// school_admin.js
document.addEventListener('DOMContentLoaded', function () {
    var latitude = document.getElementById('id_latitude').value;
    var longitude = document.getElementById('id_longitude').value;

    // Initialize the map
    var map = L.map('map').setView([latitude, longitude], 15);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Add marker for the school location
    var marker = L.marker([latitude, longitude]).addTo(map);
});
