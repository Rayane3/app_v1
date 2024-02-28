function submitLoginForm(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    const username = document.getElementById('usernameModal').value;
    const password = document.getElementById('passwordModal').value;

    // Perform AJAX request to the login route
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => {
        if (!response.ok) {
            // If the response is not OK, throw an error
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();  // Parse the JSON in the response
    })
    .then(data => {
        // Handle the response data
        if (data.success) {
            // If login is successful, redirect to the booking page
            window.location.href = '/booking';
        } else {
            // If login is not successful, display the error message
            alert(data.message);
        }
    })
    .catch(error => {
        // Catch and display any errors that occurred during the fetch
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    });
}