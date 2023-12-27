export const calculateSumMark = (criteriaMarks) => {
  let result = {
    summ: 0,
    mark: 'N/A',
  }
  if (!criteriaMarks.length) {
    return result
  }
  criteriaMarks.forEach(item => {
    result.summ += item.mark;
  })
  result.mark = calculateCriterion(criteriaMarks.length, result.summ)
  return result
}

export const calculateCriterion = (count, summ) => {
  const GRADES = { 1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28] }
  if (GRADES[count] === undefined) {
    return "N/A"
  }
  if (summ >= GRADES[count][2]) {
    return 5
  } else if (summ < GRADES[count][2] && summ >= GRADES[count][1]) {
    return 4
  } else if (summ < GRADES[count][1] && summ >= GRADES[count][0]) {
    return 3
  } else if (summ < GRADES[count][0] && summ > 0) {
    return 2
  } else {
    return '-'
  }
}
