export const truncateText = (text, maxLength) => {
  if (text && text.length > maxLength) {
    return text.substring(0, maxLength) + '...'; // или используйте text.slice(0, maxLength) + '...'
  } else {
    return text;
  }
}

export const pluralizeRu = (n, wordForms) => {
  n = Math.abs(n) % 100;
  var n1 = n % 10;
  if (n > 10 && n < 20) { return wordForms[2]; }
  if (n1 > 1 && n1 < 5) { return wordForms[1]; }
  if (n1 == 1) { return wordForms[0]; }
  return wordForms[2];
}