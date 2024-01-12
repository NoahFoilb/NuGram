document.getElementById('uploadPostForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const userId = localStorage.getItem('userID'); // Assuming userID is stored in localStorage
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('caption', document.getElementById('postCaption').value);
    formData.append('post_image', document.getElementById('postImage').files[0]);

    fetch('http://127.0.0.1:5000/create_post', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to upload post. Make sure to add caption and post image');
    });

    
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});
