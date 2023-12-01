import { isEmpty, currentReportPeriod, currentGroup, currentStudyYear, reportStore, authStore, getStudentMentorReports } from "./ReportMentorView.vue";

// Запрос на создание репорта для студента:
// Нужно выбрать период и класс
// После успешного ответа происходит повторный запрос на обновление списка студентов
export const createStudentMentorReport = (id) => {
// console.log('Запрос на создание репорта для студента')
if (isEmpty(currentReportPeriod.value) || isEmpty(currentGroup.value)) {
return null;
}
if (currentStudyYear.value.level == "noo") {
reportStore
.createReportMentorPrimary({
student: id,
author: authStore.user.id,
period: currentReportPeriod.value.id,
group: currentGroup.value.id,
})
.then((result) => {
// console.log('Репорт успешно добавлен: ', result)
getStudentMentorReports();
});
} else {
reportStore
.createReportMentor({
student: id,
author: authStore.user.id,
period: currentReportPeriod.value.id,
group: currentGroup.value.id,
})
.then((result) => {
// console.log('Репорт успешно добавлен: ', result)
getStudentMentorReports();
});
}
};
