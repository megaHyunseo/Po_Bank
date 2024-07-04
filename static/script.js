document.addEventListener('DOMContentLoaded', (event) => {
    function fetchDistance() {
        fetch('/distance')
        .then(response => response.json())
        .then(data => {
            document.getElementById('distance').innerText = `Current Distance: ${data.distance} cm`;
            if (data.distance <= 10) {
                window.location.href = '/upload';
            }
        })
        .catch(error => console.error('Error:', error));
    }

    setInterval(fetchDistance, 1000);
});
