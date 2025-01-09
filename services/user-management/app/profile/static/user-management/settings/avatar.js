function previewProfilePic(event) {
    // Get the file selected by the user
    const file = event.target.files[0];
    
    if (file) {
        // Create a new FormData object to send the file via AJAX
        const formData = new FormData();
        formData.append('avatar', file);

        // Create the URL for the API endpoint using the user ID
        const apiUrl = `/api/player/${document.querySelector('[name=playerId]').value}/avatar/`;
        
        // Create the fetch request to send the file
        fetch(apiUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken  // Assuming CSRF token handling
            }
        })
        .then(response => {
            const profilePic = document.getElementById('profile-pic');
            profilePic.src = `/api/player/${document.querySelector('[name=playerId]').value}/avatar/?${+ new Date().getTime()}`;
        })
        .catch(error => {
            console.error('Error updating profile picture:', error);
            alert('An error occurred while updating your profile picture.');
        });
    } else {
        alert('No file selected');
    }
}


