document.getElementById('locationDateForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const date = document.getElementById('date').value;

    // Display the values (you can replace this with your desired functionality)
    alert(`Latitude: ${latitude}\nLongitude: ${longitude}\nDate: ${date}`);
});