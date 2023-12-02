export const EMAIL_REGEX =
  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;


export const MARK5 = [
  { value: null, name: "Н/A" },
  { value: 2, name: "2" },
  { value: 3, name: "3" },
  { value: 4, name: "4" },
  { value: 5, name: "5" },
]

export const MARK8 = [
  { value: null, name: "-" },
  { value: 0, name: "0" },
  { value: 1, name: "1" },
  { value: 2, name: "2" },
  { value: 3, name: "3" },
  { value: 4, name: "4" },
  { value: 5, name: "5" },
  { value: 6, name: "6" },
  { value: 7, name: "7" },
  { value: 8, name: "8" },
]

export const MARK7 = [
  { value: null, name: "-" },
  { value: 0, name: "0" },
  { value: 1, name: "1" },
  { value: 2, name: "2" },
  { value: 3, name: "3" },
  { value: 4, name: "4" },
  { value: 5, name: "5" },
  { value: 6, name: "6" },
  { value: 7, name: "7" },
]

export const REPORT_TYPES = [
  { value: 'noo', name: 'Репорты начальной школы' },
  { value: 'ooo', name: 'Репорты средней школы' },
  { value: 'soo', name: 'Репорты старшей школы' },
  { value: 'dp', name: 'Репорты старшей школы (DP)' },
]

export const PROFILE_LEVELS = [
  { value: 'low', name: 'Слегка выражено' },
  { value: 'medium', name: 'Выражено' },
  { value: 'high', name: 'Выражено в сильной степени' },
  { value: null, name: 'Не указано' },
]