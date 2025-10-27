// static/vault/js/main.js
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(function() {
    alert('Copied to clipboard — it will be cleared from clipboard in 30s manually (browser behavior may vary).');
  }, function(err) {
    console.error('Could not copy: ', err);
  });
}
