export const truncateText = (text, maxLength) => {
  if (text && text.length > maxLength) {
    return text.substring(0, maxLength) + '...'; // или используйте text.slice(0, maxLength) + '...'
  } else {
    return text;
  }
}