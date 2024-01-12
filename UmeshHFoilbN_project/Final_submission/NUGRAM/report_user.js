document.getElementById('reportForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const reportedId = document.getElementById('reportedId').value;
    const reportCategory = document.getElementById('reportCategory').value;
    const reportDescription = document.getElementById('reportDescription').value;
    const reporterId = localStorage.getItem('NUID'); // Retrieve the reporter's ID from local storage
    const messageDate = new Date().toISOString();

    fetch('http://127.0.0.1:5000/submit_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            reporter_id: reporterId,
            reported_id: reportedId,
            report_category: reportCategory,
            report_description: reportDescription,
            report_time: messageDate
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();  // Parse JSON only if the response is ok
        } else {
            throw new Error('Failed to submit report');
        }
    })
    .then(data => {
        alert('Report submitted successfully');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to submit report: ' + error.message);
    });
});

document.getElementById('dashboardButton').addEventListener('click', function() {
    window.location.href = 'dashboard.html';
});

document.getElementById('oldreportsButton').addEventListener('click', function() {
    window.location.href = 'list_reports.html';
});
