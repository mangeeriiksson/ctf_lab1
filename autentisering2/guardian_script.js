document.getElementById('challenge-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    const code = document.getElementById('code').value;

    // Skicka inmatning till servern för validering
    fetch('/validate_offering', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password, code }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('feedback').innerText = data.message;
    });
});
