export const formatDate = (string) => {
  const date = new Date(string);
  const day = date.getDate();
  const month = date.getMonth() + 1; // Месяцы начинаются с 0
  const year = date.getFullYear();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();

  return `${day.toString().padStart(2, '0')}.${month.toString().padStart(2, '0')}.${year} ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

export const formatToYYYYMMDD = (date) => {
  const d = new Date(date);
  let month = '' + (d.getMonth() + 1); // getMonth() возвращает месяцы от 0 до 11
  let day = '' + d.getDate();
  const year = d.getFullYear();

  if (month.length < 2) 
    month = '0' + month;
  if (day.length < 2) 
    day = '0' + day;

  return [year, month, day].join('-');
}

export const formatDateToReadable = (dateString) => {
  const options = { year: 'numeric', month: 'numeric', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('ru-RU', options);
}