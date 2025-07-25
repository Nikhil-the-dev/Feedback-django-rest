
// Function to toggle the visibility of the search box
function toggleSearchBox() {
    const searchBox = document.getElementById('searchBox');
    searchBox.classList.toggle('open');  // Toggle the 'open' class to slide it in/out
}

function text_search(data) {
    const table = document.getElementById('feedbackTable');
    const rows = table.querySelectorAll('.feedback-row');

    // If search input is empty, show all feedback rows
    if (data.trim() === '') {
        rows.forEach(row => {
            row.style.display = '';
        });
    } else {
        // Hide rows that do not match the search query
        rows.forEach(row => {
            const feedbackDescription = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
            if (feedbackDescription.includes(data.toLowerCase())) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
}
