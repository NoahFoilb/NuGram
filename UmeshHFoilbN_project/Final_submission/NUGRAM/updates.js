function promptUpdate(field) {
    const newValue = prompt(`Enter new ${field}:`);
    if (newValue) {
        updateUserDetails(field, newValue);
    }
}

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

function updateUserDetails(field, value) {
    const userId = localStorage.getItem('userID'); // Replace with actual user identification logic

    fetch('http://127.0.0.1:5000/update_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            field: field,
            value: value
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
