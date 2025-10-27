// vault/static/vault/js/main.js

// Copy to clipboard helper
function copyToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopy(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
    alert('Copied to clipboard');
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
    alert('Could not copy to clipboard');
  });
}

function fallbackCopy(text) {
  var textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.left = '-9999px';
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand('copy');
    alert('Copied to clipboard');
  } catch (err) {
    alert('Unable to copy');
  }
  document.body.removeChild(textarea);
}

// Simple password generator
function generatePassword(length=16, useNumbers=true, useSymbols=true) {
  var lower = "abcdefghijklmnopqrstuvwxyz";
  var upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var numbers = "0123456789";
  var symbols = "!@#$%^&*()-_=+[]{};:,.<>/?";
  var chars = lower + upper;
  if (useNumbers) chars += numbers;
  if (useSymbols) chars += symbols;

  var pwd = "";
  for (var i = 0; i < length; i++) {
    pwd += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return pwd;
}

// Password strength basic estimator
function passwordScore(pwd) {
  var score = 0;
  if (!pwd) return 0;
  if (pwd.length >= 8) score += 1;
  if (pwd.length >= 12) score += 1;
  if (/[A-Z]/.test(pwd)) score += 1;
  if (/[0-9]/.test(pwd)) score += 1;
  if (/[^A-Za-z0-9]/.test(pwd)) score += 1;
  return score; // 0-5
}
