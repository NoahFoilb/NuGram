document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value;
    searchUsers(searchTerm);
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});


function searchUsers(searchTerm) {
    fetch('http://127.0.0.1:5000/search_users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ search: searchTerm })
    })
    .then(response => response.json())
    .then(users => displaySearchResults(users))
    .catch(error => console.error('Error:', error));
}

function displaySearchResults(users) {
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.innerHTML = `Name: ${user.first_name} ${user.last_name}`;

        const messageButton = document.createElement('button');
        messageButton.innerText = 'Message';
        messageButton.onclick = () => checkFollowStatusAndMessage(user.user_id);
        userDiv.appendChild(messageButton);

        resultsContainer.appendChild(userDiv);
    });
}



function showMessageSection(userId) {
    const currentUserId = localStorage.getItem('userID');
    if (currentUserId) {
        document.getElementById('messagingSection').style.display = 'block';
        loadMessages(currentUserId, userId);
        document.getElementById('sendMessageButton').onclick = () => sendMessage(currentUserId, userId);
    } else {
        alert('Please log in to send messages');
    }
}

function checkFollowStatusAndMessage(followedUserId) {
    const currentUserId = localStorage.getItem('userID');
    fetch(`http://127.0.0.1:5000/check_follow_status/${currentUserId}/${followedUserId}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.follows) {
            showMessageSection(followedUserId);
        } else {
            alert('You do not follow this user. Redirecting to follow page.');
            window.location.href = 'follow.html';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}



function loadMessages(senderId, receiverId) {
    fetch(`http://127.0.0.1:5000/get_messages/${senderId}/${receiverId}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(messages => {
        const messageList = document.getElementById('messageList');
        messageList.innerHTML = ''; // Clear previous messages

        messages.forEach(message => {
            const messageSenderName = message.sender_id === senderId ? 'You' : message.sender_first_name;
            const messageDiv = document.createElement('div');
            messageDiv.innerHTML = `
                <p>${messageSenderName}: ${message.message_body}</p>
                <small>${new Date(message.message_date).toLocaleString()}</small>
            `;
            messageList.appendChild(messageDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



function sendMessage(senderId, receiverId) {
    const messageBody = document.getElementById('messageInput').value;
    const messageDate = new Date().toISOString();

    fetch('http://127.0.0.1:5000/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sender_id: senderId,
            receiver_id: receiverId,
            message_body: messageBody,
            message_date: messageDate
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Message sent successfully');
            document.getElementById('messageInput').value = ''; // Clear input field
            loadMessages(senderId, receiverId); // Reload messages to display the new one
        } else {
            alert('Failed to send message');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

