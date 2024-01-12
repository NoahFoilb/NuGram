document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

// Fetch and display groups
function displayGroups() {
    fetch('http://127.0.0.1:5000/get_groups')
    .then(response => response.json())
    .then(groups => {
        const groupsList = document.getElementById('groupsList');
        groups.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.innerHTML = `
                <h4>${group.group_name}</h4>
                <p>${group.description}</p>
                <img src="data:image/jpeg;base64,${group.group_image}" style="width: 100px; height: 100px;">
            `;
            groupsList.appendChild(groupDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




// Handle join group form submission
document.getElementById('joinGroupForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const groupName = document.getElementById('groupName').value;
    const NUID = localStorage.getItem('NUID');

    fetch('http://127.0.0.1:5000/join_group', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ NUID: NUID, group_name: groupName })
    })
    .then(response => {
        if (response.ok) {
            alert('Successfully joined the group!');
        } else {
            alert('Failed to join the group');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});



// Initial call to display groups
displayGroups();
