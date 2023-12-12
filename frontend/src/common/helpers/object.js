export const extractIds = (obj) => {
  let newObj = {}
  for (let key in obj) {
    if (Array.isArray(obj[key])) {
      newObj[key] = obj[key].map(item => item.id)
    } else if (obj[key] !== null && typeof obj[key] === 'object') {
      newObj[key] = obj[key].id
    } else {
      newObj[key] = obj[key]
    }
  }
  return newObj
}