function fetchTimetable() {
    const place = document.getElementById('timetablePlace').value;
    if (!place) {
        document.getElementById('timetable').innerHTML = '';
        return;
    }

    fetch(`/fetch_timetable?place=${encodeURIComponent(place)}`)
        .then(response => response.json())
        .then(data => {
            const timetableDiv = document.getElementById('timetable');
            timetableDiv.innerHTML = ''; // Clear previous entries
            data.reservations.forEach(reservation => {
                const entry = document.createElement('div');
                entry.className = 'timetable-entry';
                entry.textContent = `Date: ${reservation.date}, Time: ${reservation.start_time} - ${reservation.end_time}`;
                timetableDiv.appendChild(entry);
            });
        })
        .catch(error => console.error('Error fetching timetable:', error));
}
