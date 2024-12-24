document.getElementById('shorten').addEventListener('click', function() {
  const url = document.getElementById('url').value;

  fetch('https://maskurl.pythonanywhere.com/add_url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.getElementById('shortenedUrl').textContent = data.short_url;
      document.getElementById('qrCode').src = `data:image/png;base64,${data.qr_code}`;
    } else {
      alert(data.message);
    }
  })
  .catch(error => {
    console.error('Error shortening URL:', error);
  });
});
