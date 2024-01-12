document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value;
    searchUsers(searchTerm);
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

document.getElementById('followersButton').addEventListener('click', function() {
    const currentUserId = localStorage.getItem('userID');
    if (currentUserId) {
        fetchFollowers(currentUserId);
    } else {
        alert('No user is logged in');
    }
});

document.getElementById('followingButton').addEventListener('click', function() {
    const currentUserId = localStorage.getItem('userID');
    if (currentUserId) {
        fetchFollowing(currentUserId);
    } else {
        alert('No user is logged in');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const currentUserId = localStorage.getItem('userID');
    if (currentUserId) {
        console.log('Logged in User ID:', userID);
        // Perform actions that require the user ID
    } else {
        console.log('No user is logged in');
        // Redirect to login page or handle accordingly
    }
});

function fetchFollowers(userId) {
    fetch(`http://127.0.0.1:5000/get_followers/${userId}`)
    .then(response => response.json())
    .then(followers => {
        displayFollowers(followers);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayFollowers(followers) {
    const followersList = document.getElementById('followersList');
    followersList.innerHTML = ''; // Clear existing list

    followers.forEach(follower => {
        const followerDiv = document.createElement('div');
        followerDiv.innerHTML = `Name: ${follower.first_name} ${follower.last_name}`;
        followersList.appendChild(followerDiv);
    });
}

function fetchFollowing(userId) {
    fetch(`http://127.0.0.1:5000/get_following/${userId}`)
    .then(response => response.json())
    .then(following => {
        displayFollowing(following);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/*
function displayFollowing(following) {
    const followingList = document.getElementById('followingList');
    followingList.innerHTML = ''; // Clear existing list

    following.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.innerHTML = `Name: ${user.first_name} ${user.last_name}`;
        followingList.appendChild(userDiv);
    });
}
*/


function displayFollowing(following) {
    const followingList = document.getElementById('followingList');
    followingList.innerHTML = ''; // Clear existing list

    following.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.innerHTML = `Name: ${user.first_name} ${user.last_name}`;

        // Add Unfollow button
        const unfollowButton = document.createElement('button');
        unfollowButton.innerText = 'Unfollow';
        unfollowButton.onclick = () => unfollowUser(localStorage.getItem('userID'), user.user_id);
        userDiv.appendChild(unfollowButton);

        followingList.appendChild(userDiv);
    });
}

function unfollowUser(followerId, followedId) {
    // Implement unfollow logic
    fetch(`http://127.0.0.1:5000/unfollow_user`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ follower_id: followerId, followed_id: followedId })
    })
    .then(response => {
        if (response.ok) {
            alert('You have unfollowed this user');
            // Optionally, refresh the following list
        } else {
            alert('Failed to unfollow user');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
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

function followUser(followerId, followedId) {
    const followData = {
        follower_id: followerId,
        followed_id: followedId,
        follow_date: new Date().toISOString()
    };

    fetch('http://127.0.0.1:5000/follow_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(followData)
    })
    .then(response => {
        if (response.ok) {
            alert('You now follow this user');
        } else {
            alert('Failed to follow user');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function getCurrentUserId() {
    return fetch('http://127.0.0.1:5000/get_current_user')
        .then(response => response.json())
        .then(data => {
            if (data && data.user_id) {
                return data.user_id;
            } else {
                throw new Error('User not logged in');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


