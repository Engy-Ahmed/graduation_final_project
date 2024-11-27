// Add an event listener to the form submission event
document.getElementById('upload-form').addEventListener('submit', function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();
    
    // Get the file input element
    var fileInput = document.getElementById('file-selector');
    
    // Get the selected file
    var file = fileInput.files[0];
    
    // Create a FormData object to send the file data
    var formData = new FormData();
    formData.append('file', file);
    
    // Send a POST request to the predict route with the file data
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    // Parse the JSON response
    .then(response => response.json())
    // Handle the response data
    .then(data => {
        // Get the result div element
        var resultDiv = document.getElementById('result');
        // If there is an error in the response
        if (data.error) {
            // Display the error message in the result div
            resultDiv.innerText = data.error;
        } else {
            // Determine the result text based on the prediction class
            var resultText;
            if (data.class == 0) {
                resultText = 'Benign';
            } else if (data.class == 1) {
                resultText = 'Malignant';
            } else {
                // If the prediction is unknown, display a custom message
                resultText = 'The type of cancer could not be determined.';
            }
            // Display the prediction result in the result div
            resultDiv.innerText = 'Prediction: ' + resultText;
        }
    })
    // Handle any errors that occur during the fetch request
    .catch(error => {
        console.error('Error:', error);
    });
});
