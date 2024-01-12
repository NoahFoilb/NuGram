document.addEventListener('DOMContentLoaded', () => {
    fetchFollowedUsersPosts();
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

function fetchFollowedUsersPosts() {
    const userId = localStorage.getItem('userID');
    if (!userId) {
        console.error('No user is logged in');
        return;
    }

    fetch(`http://127.0.0.1:5000/get_followed_users_posts/${userId}`)
    .then(response => response.json())
    .then(posts => {
        displayPosts(posts);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function displayPosts(posts) {
    const postsContainer = document.getElementById('postsContainer');
    postsContainer.innerHTML = ''; // Clear existing content

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.classList.add('post');
        postDiv.innerHTML = `
            <h3>${post.caption}</h3>
            <img src="data:image/jpeg;base64,${post.post}" style="width: 100px; height: 100px;">
            <p>Likes: ${post.like_count}</p>
            <button onclick="toggleLike(${post.post_id})">Like/Unlike</button>
            <button onclick="toggleComments(${post.post_id})">Show/Hide Comments</button>
            <div class="comments" id="comments-${post.post_id}" style="display: none;">
                ${post.comments.map(comment => `<p>${comment.first_name}: ${comment.comment}</p>`).join('')}
                <input type="text" id="comment-input-${post.post_id}" placeholder="Add a comment">
                <button onclick="addComment(${post.post_id})">Comment</button>
            </div>
        `;
        postsContainer.appendChild(postDiv);
    });
}



function toggleLike(postId) {
    // Assuming that the user ID is stored in localStorage
    const userId = localStorage.getItem('userID');

    fetch(`http://127.0.0.1:5000/toggle_like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, post_id: postId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Optionally, refresh the post to update like count
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function toggleComments(postId) {
    const commentsDiv = document.getElementById(`comments-${postId}`);
    if (commentsDiv.style.display === 'none') {
        commentsDiv.style.display = 'block';
    } else {
        commentsDiv.style.display = 'none';
    }
}

function addComment(postId) {
    const userId = localStorage.getItem('userID');
    const commentInput = document.getElementById(`comment-input-${postId}`);
    const commentText = commentInput.value;

    fetch(`http://127.0.0.1:5000/add_comment`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, post_id: postId, comment: commentText })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        commentInput.value = ''; // Clear the input field
        // Optionally, refresh the post to show the new comment
    })
    .catch(error => {
        console.error('Error:', error);
    });

    
}


