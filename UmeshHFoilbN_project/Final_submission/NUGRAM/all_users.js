document.addEventListener('DOMContentLoaded', () => {
    getAllUsers();


    document.getElementById('dashboardButton').addEventListener('click', function() {
        window.location.href = 'dashboard.html';
    });
});

document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value;
    searchUsers(searchTerm);
});

function getAllUsers() {
    fetch('http://127.0.0.1:5000/get_all_users')
    .then(response => response.json())
    .then(users => displayUsers(users))
    .catch(error => console.error('Error:', error));
}

function displayUsers(users) {
    const container = document.getElementById('usersContainer');
    container.innerHTML = ''; // Clear existing users

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-div';
        userDiv.innerHTML = `
          <div class="user-info">
            <p>Name: ${user.first_name} ${user.last_name}</p>
            <p>Email: ${user.email}</p>
            <p>Phone: ${user.phone_number || 'N/A'}</p>
            <p>Degree: ${user.degree}</p>
            <p>Major: ${user.major}</p>
            <p>College: ${user.college}</p>
          </div>  
        `;

        // Add profile picture if available
        if (user.profile_picture) {
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${user.profile_picture}`;
            img.style.width = '100px';
            img.style.height = '100px';
            userDiv.appendChild(img);
        }

        container.appendChild(userDiv);
    });
}


function searchUsers(searchTerm) {
    fetch('http://127.0.0.1:5000/search_users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ search: searchTerm })
    })
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function displaySearchResults(users) {
    // Clear the full user list when displaying search results
    const allUsersContainer = document.getElementById('usersContainer');
    allUsersContainer.innerHTML = '';

    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = ''; // Clear previous results

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.innerHTML = `Name: ${user.first_name} ${user.last_name}`;
        if (user.profile_picture) {
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${user.profile_picture}`;
            img.style.width = '100px';
            img.style.height = '100px';
            userDiv.appendChild(img);
        }

        // Add follow button
        const currentUserId = localStorage.getItem('userID');
        const followButton = document.createElement('button');
        followButton.innerText = 'Follow';
        followButton.onclick = () => followUser(currentUserId, user.user_id); 
        userDiv.appendChild(followButton);

        resultsContainer.appendChild(userDiv);
    });
}
