document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const imageInput = document.getElementById('imageInput');
    const resultDiv = document.getElementById('result');
    const txHashDiv = document.getElementById('txHash');
    const previewImg = document.getElementById('previewImg');
    const imagePreviewDiv = document.getElementById('imagePreview');

    // Handle Image Upload & Prediction
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const file = imageInput.files[0];
        if (!file) {
            alert("Please select an image!");
            return;
        }

        resultDiv.textContent = "Processing...";
        txHashDiv.textContent = "";

        // Resize image using canvas
        const resizedBlob = await resizeImage(file, 200, 190);

        const formData = new FormData();
        formData.append('image', resizedBlob, 'resized_image.jpg');

        // Show image preview
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            imagePreviewDiv.style.display = 'block';
        };
        reader.readAsDataURL(resizedBlob);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            resultDiv.textContent = "Predicted Stage: " + data.predicted_class;
            txHashDiv.innerHTML = `Transaction Hash: <a href="https://etherscan.io/tx/${data.transaction_hash}" target="_blank">${data.transaction_hash}</a>`;
        } catch (err) {
            resultDiv.textContent = "Error during processing.";
            console.error(err);
        }
    });

    // Resize helper using canvas
    async function resizeImage(file, width, height) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            const canvas = document.createElement('canvas');
            const reader = new FileReader();

            reader.onload = e => {
                img.onload = () => {
                    canvas.width = width;
                    canvas.height = height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);
                    canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.95);
                };
                img.src = e.target.result;
            };

            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    // (Optional) Handle TX Hash Metadata Retrieval
    const txHashForm = document.getElementById('txHashForm');
    const txHashInput = document.getElementById('txHashInput');
    const txResultDiv = document.getElementById('txResult');

    if (txHashForm) {
        txHashForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const txHash = txHashInput.value.trim();
            if (!txHash) {
                alert("Please enter a valid transaction hash.");
                return;
            }

            txResultDiv.textContent = "Fetching metadata...";

            try {
                const response = await fetch('/get_metadata', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tx_hash: txHash })
                });

                const data = await response.json();

                if (data.error) {
                    txResultDiv.textContent = "Error: " + data.error;
                } else {
                    txResultDiv.textContent = "Metadata: " + data.metadata;
                }
            } catch (err) {
                txResultDiv.textContent = "Error during metadata fetch.";
                console.error(err);
            }
        });
    }
});
