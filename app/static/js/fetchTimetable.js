function fetchTimetable() {
    const place = document.getElementById('timetablePlace').value;
    if (!place) {
        document.getElementById('timetable').innerHTML = '';
        return;
    }

    fetch(`/fetch_timetable?place=${encodeURIComponent(place)}`)
        .then(response => response.json())
        .then(data => {
            const timetableGrid = document.querySelector('.timetable-grid');

            // Assuming data.reservations is an array of reservation objects
            data.reservations.forEach(reservation => {
                // Find the slot that corresponds to the reservation's date and time
                const slotSelector = `.day-slot[data-date="${reservation.date}"][data-time="${reservation.start_time}"]`;
                const slot = timetableGrid.querySelector(slotSelector);

                // If a slot exists, mark it as booked
                if (slot) {
                    slot.classList.remove('available');
                    slot.classList.add('booked');
                    slot.textContent = 'Booked';
                }
            });
        })
        .catch(error => console.error('Error fetching timetable:', error));
}
