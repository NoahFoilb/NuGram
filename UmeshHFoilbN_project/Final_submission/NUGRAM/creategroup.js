
document.getElementById('createGroupForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('group_name', document.getElementById('groupName').value);
    formData.append('description', document.getElementById('description').value);
    var groupImage = document.getElementById('groupImage').files[0];
    formData.append('group_image', groupImage);

    fetch('http://127.0.0.1:5000/create_group', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Group created successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to create group.');
    });
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

