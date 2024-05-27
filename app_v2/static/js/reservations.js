// Function to update a reservation
function updateReservation(rowElement) {
    const reservationId = rowElement.getAttribute('data-id');
    const bookedPlace = rowElement.querySelector('.booked-place').textContent;
    const dateOfReservation = rowElement.querySelector('.date-of-reservation').textContent;
    const startTime = rowElement.querySelector('.start-time').textContent;
    const endTime = rowElement.querySelector('.end-time').textContent;

    // Fill the modal inputs with the current reservation details
    document.getElementById('updateReservationId').value = reservationId;
    document.getElementById('updateBookedPlace').value = bookedPlace;
    document.getElementById('updateReservationDate').value = dateOfReservation;
    document.getElementById('updateStartTime').value = startTime;
    document.getElementById('updateEndTime').value = endTime;

    // Show the modal
    var updateModal = new bootstrap.Modal(document.getElementById('updateReservationModal'));
    updateModal.show();
}

function submitUpdateReservation() {
    const reservationId = document.getElementById('updateReservationId').value;
    const bookedPlace = document.getElementById('updateBookedPlace').value;
    const dateOfReservation = document.getElementById('updateReservationDate').value;
    const startTime = document.getElementById('updateStartTime').value;
    const endTime = document.getElementById('updateEndTime').value;

    // Prepare the data to be sent in the request
    const data = {
        booked_place: bookedPlace,
        date_of_reservation: dateOfReservation,
        time_of_reservation: startTime,
        end_time_of_reservation: endTime,
    };

    // Send a POST request to the update endpoint
    fetch(`/update_reservation/${reservationId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Reservation updated successfully');
        location.reload(); // Refresh the page to show the updated list
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while updating the reservation.');
    });

    // Hide the modal after submission
    var updateModal = bootstrap.Modal.getInstance(document.getElementById('updateReservationModal'));
    updateModal.hide();
}


// Function to delete a reservation
function deleteReservation(reservationId) {
    // Send a POST request to the delete endpoint
    fetch(`/delete_reservation/${reservationId}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        // Handle response
        console.log('Success:', data);
        alert('Reservation deleted successfully');
        // Remove the row from the table
        document.querySelector(`tr[data-id="${reservationId}"]`).remove();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while deleting the reservation.');
    });
}
