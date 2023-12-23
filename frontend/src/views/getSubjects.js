import { isEmpty, currentGroup, authStore, curriculumStore, currentSubject, resetSelectedSubject } from "./ReportTeacherView.vue";

// Запрос на получение списка учебных планов (срабатывает, если выбран учебный план и групппа)
export const getSubjects = () => {
if (!isEmpty(currentGroup.value)) {
let config = {
params: {
curriculum_loads__years__classes: currentGroup.value.id,
}
};
if (!authStore.isAdmin) {
config.params.teaching_loads__teacher = authStore.user.id;
config.params.teaching_loads__groups = [currentGroup.value.id];
}
curriculumStore.loadSubjects(config).then((result) => {
if (!curriculumStore.subjects.map(i => i.id).includes(currentSubject.value.id))
resetSelectedSubject();
});
}
};
