// document.getElementById('sendButton').addEventListener('click', () => {
//     const sentence = document.getElementById('sentenceInput').value;

//     if (sentence.trim() === '') {
//         alert('Please enter a sentence');
//         return;
//     }

//     // Send the sentence to the Flask API using fetch (POST request)
//     fetch('/process-stock-data', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ prompt: sentence })  // Send the sentence as JSON
//     })
//         .then(response => response.json())  // Parse the JSON response
//         .then(data => {
//             console.log(data);

//             // Display the server response message
//             document.getElementById('responseMessage').textContent = `Server response: ${data.message}`;

//             // Display the sentence sent
//             document.getElementById('responseSentence').textContent = `${data.data}`;

//             // Display the base64 image in the img tag
//             const imgElement = document.getElementById('responseImage');
//             imgElement.src = 'data:image/png;base64,' + data.image;  // Embed the base64 image in the src attribute
//             // Enable the download button after the image is displayed
//             const downloadButton = document.getElementById('downloadButton');
//             downloadButton.style.display = 'inline';  // Show the download button

//             // Handle image download
//             downloadButton.addEventListener('click', () => {
//                 const link = document.createElement('a');
//                 link.href = imgElement.src;  // Use the image source as the download link
//                 link.download = 'stock_image.png';  // Set the download filename
//                 link.click();  // Trigger the download
//             });
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             document.getElementById('responseMessage').textContent = 'An error occurred!';
//         });
// });

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('sendButton').addEventListener('click', () => {
        const sentence = document.getElementById('sentenceInput').value;

        if (sentence.trim() === '') {
            alert('Please enter a sentence');
            return;
        }

        // Send the sentence to the Flask API using fetch (POST request)
        fetch('/process-stock-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: sentence }), // Send the sentence as JSON
        })
            .then(response => response.json()) // Parse the JSON response
            .then(data => {
                console.log(data);

                // Display the server response message
                document.getElementById('responseMessage').textContent = `Server response: ${data.message}`;

                // Display the sentence sent
                document.getElementById('responseSentence').textContent = `${data.data}`;

                // Display the base64 image in the img tag
                const imgElement = document.getElementById('responseImage');
                imgElement.src = 'data:image/png;base64,' + data.image; // Embed the base64 image in the src attribute

                // Enable the download button after the image is displayed
                const downloadButton = document.getElementById('downloadButton');
                if (downloadButton) {
                    downloadButton.style.display = 'inline'; // Show the download button

                    // Handle image download
                    downloadButton.addEventListener('click', () => {
                        const link = document.createElement('a');
                        link.href = imgElement.src; // Use the image source as the download link
                        link.download = 'stock_image.png'; // Set the download filename
                        link.click(); // Trigger the download
                    });
                } else {
                    console.error('Download button not found!');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('responseMessage').textContent = 'An error occurred!';
            });
    });
});
