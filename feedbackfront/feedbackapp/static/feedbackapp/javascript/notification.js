// notification.js

window.onload = function() {
    if (document.getElementById("message-box")) {
        // Show notification and then hide after 3 seconds
        setTimeout(function () {
            const messageBox = document.getElementById("message-box");
            if (messageBox) {
                messageBox.classList.add('show');  // Show the notification
            }

            // Hide the message and redirect after 3 seconds
            setTimeout(function () {
                if (messageBox) {
                    messageBox.classList.add('hide'); // Hide the notification
                }

                // Redirect to another page (modify the URL as needed)
                // window.location.href = "new-page.html"; // Uncomment to enable redirection

            }, 2000);  // Hide after 2 seconds
        }, 100);  // Show after 100ms
    }
};
