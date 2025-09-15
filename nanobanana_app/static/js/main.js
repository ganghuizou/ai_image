document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', async () => {
            const prompt = document.getElementById('prompt').value;
            const resultImg = document.getElementById('result-img');

            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt }),
            });

            const data = await response.json();

            if (data.image_url) {
                resultImg.src = data.image_url;
            } else {
                alert(data.error || 'An unknown error occurred.');
            }
        });
    }
});