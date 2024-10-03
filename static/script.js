document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const pdfFile = document.getElementById('pdfFile').files[0];
    const formData = new FormData();
    formData.append('file', pdfFile);

    const response = await fetch('/upload_pdf', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    alert(result.message || result.error);

    if (response.ok) {
        document.getElementById('questionSection').style.display = 'block'; // 顯示提問區域
    }
});

document.getElementById('askButton').addEventListener('click', async function() {
    const question = document.getElementById('questionInput').value;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    });

    const result = await response.json();
    document.getElementById('answerOutput').textContent = result.answer || result.error;
});
