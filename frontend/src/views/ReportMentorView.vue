<template>
  <div>
    <h1>Репорты руководителя класса</h1>
    <div class="py-2">
      <div class="d-flex flex-wrap">
        <div class="m-2">
          <simple-dropdown title="Выберите учебный год" v-model="currentAcademicYear"
            :propItems="generalStore.academicYears" showName="name" @select="selectAcademicYear" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите период" v-model="currentReportPeriod" :propItems="filteredReportPeriod"
            showName="full_name" :disabled="!Boolean(filteredReportPeriod.length)" @select="selectReportPeriod" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите параллель" v-model="currentStudyYear" :propItems="generalStore.studyYears"
            showName="name" @select="selectStudyYear" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите класс" v-model="currentGroup" :propItems="filteredGroup" showName="full_name"
            :disabled="isEmpty(currentAcademicYear) || isEmpty(currentStudyYear)
              " @select="selectGroup" />
        </div>
        <button type="button" class="btn btn-secondary m-2" @click="resetSelectedOptions">
          Сброс
        </button>
      </div>
      <button type="button" class="btn btn-primary m-2" @click="getStudentMentorReports"
        :disabled="isEmpty(currentGroup) || isEmpty(currentReportPeriod)">
        Показать студентов
      </button>
      <hr class="hr" />
      <div class="text-bg-light p-2 rounded">
        <h5 v-if="!isEmpty(currentStudyYear)" class="mb-2">
          Тип репорта: {{ currentReportType.name }}
        </h5>
      </div>
      <div v-if="reportStore.studentMentorReports.length" class="row">
        <div class="col-md-3">
          <div class="d-flex flex-column align-items-start justify-content-start m-2 sticky-top list-right-student">
            <div v-if="!isEmpty(currentGroup)">
              <h5>{{ currentGroup.name }} класс</h5>
              <div v-if="currentGroup.mentor">{{ currentGroup.mentor.short_name }}</div>
              <hr />
            </div>
            <div v-for="student in reportStore.studentMentorReports" :key="student.id">
              <div class="d-flex align-items-center my-1">
                <img :src="student.photo ? student.photo : imageStudent" alt="" width="20" class="me-2 rounded-circle" />
                <a class="select" :href="`#st-${student.id}`">
                  {{ student.short_name }}
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="col pe-3">
          <div v-for="student in reportStore.studentMentorReports" :key="student.id" class="my-3"
            :id="`st-${student.id}`">
            <div class="card my-1 anchor-student">
              <div class="card-body d-flex align-items-center">
                <img :src="student.photo ? student.photo : imageStudent" alt="" width="50" class="me-2 rounded-circle" />
                <h4 class="m-0">
                  {{ student.last_name }} {{ student.first_name }}
                </h4>
                <div class="ms-auto">
                  <i class="bi bi-three-dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
                  <ul class="dropdown-menu">
                    <li v-if="!student.reports.length">
                      <a class="dropdown-item" href="##" @click="createStudentMentorReport(student.id)">Добавить репорт
                        руководителя</a>
                    </li>
                    <li v-else>
                      <a class="dropdown-item" href="##" @click="showConfirmationModal(student)">Удалить репорт
                        руководителя</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="accordion my-1" :id="`accordionStudent-${student.id}`" v-if="student.reports.length">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`heading-${student.id}`">
                  <button class="accordion-button collapsed p-2" :class="{ 'report-success': student.report.comment }"
                    type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${student.id}`"
                    aria-expanded="true" :aria-controls="`collapse-${student.id}`">
                    Репорт руководителя класса
                  </button>
                </h2>
                <div :id="`collapse-${student.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`heading-${student.id}`">
                  <div class="accordion-body">
                    <div class="my-2">
                      <report-mentor-ib-profile :report="student.report" />
                    </div>
                    <hr />
                    <div class="my-2">
                      <editable-area-tiny class="text-muted" :propData="student.report.comment" propName="comment"
                        @save="handleSave($event, student.report.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
                    </div>
                    <hr />
                    <div class="d-flex align-items-center">
                      <i class="bi bi-person"></i>
                      <div class="ms-1">
                        {{ student.report.author.short_name }}
                      </div>
                      <div class="ms-2">
                        {{ formatDate(student.report.updated_at) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion my-1" :id="`accordionStudentExtra-${student.report.id}`" v-if="student.reports.length">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`headingExtra-${student.report.id}`">
                  <button class="accordion-button collapsed p-2" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#collapseExtra-${student.report.id}`" aria-expanded="true"
                    :aria-controls="`collapseExtra-${student.report.id}`">
                    Репорты сотрудников класса
                  </button>
                </h2>
                <div :id="`collapseExtra-${student.report.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`headingExtra-${student.report.id}`">
                  <div class="accordion-body">
                    <div v-if="student.extra_reports && student.extra_reports.length">
                      <div v-for="extra in student.report_extra" :key="extra.id">
                        <div class="my-2" v-html="extra.comment"></div>
                        <hr />
                        <div class="d-flex align-items-center">
                          <i class="bi bi-person"></i>
                          <div class="ms-1">
                            {{ extra.author.short_name }}
                          </div>
                          <div class="ms-2">
                            {{ formatDate(extra.updated_at) }}
                          </div>
                        </div>
                      </div>

                    </div>
                    <div v-else>
                      Репорта не найдено!
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion my-1" :id="`accordionStudentTeacher-${student.report.id}`"
              v-if="student.reports.length">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`headingTeacher-${student.report.id}`">
                  <button class="accordion-button collapsed p-2" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#collapseTeacher-${student.report.id}`" aria-expanded="true"
                    :aria-controls="`collapseTeacher-${student.report.id}`">
                    Репорты учителей
                  </button>
                </h2>
                <div :id="`collapseTeacher-${student.report.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`headingTeacher-${student.report.id}`">
                  <div class="accordion-body">
                    <div v-if="student.report_teacher && student.report_teacher.length">
                      <div v-for="teacher in student.report_teacher" :key="teacher.id" class="my-2">
                        <div class="card">
                          <div class="card-body">
                            <div><strong>{{ teacher.subject.name }}</strong> ({{ teacher.period.name }}, {{
                              teacher.period.year.name }})</div>
                            <div class="my-2"
                              v-if="teacher.criterion_achievements && teacher.criterion_achievements.length">
                              <div v-for="cr in teacher.criterion_achievements" :key="cr.id">
                                {{ cr.criterion.name }}: <b>{{ cr.achievement.name }}</b>
                              </div>
                            </div>
                            <div class="my-2" v-if="teacher.topic_achievements && teacher.topic_achievements.length">
                              <div v-for="topic in teacher.topic_achievements" :key="topic.id">
                                {{ topic }}
                              </div>
                            </div>
                            <div class="my-2" v-if="teacher.objective_levels && teacher.objective_levels.length">
                              <div v-for="objective in teacher.objective_levels" :key="objective.id">
                                <div>
                                  <b>
                                    {{ objective.strand.objective_letter.toUpperCase() }}.{{
                                      objective.strand.strand_letter }}.
                                    Students should be able to {{ objective.strand.name }}
                                  </b>
                                </div>
                                <div class="ms-3">
                                  The student {{ objective.level.name }}:
                                  {{ objective.level.point - 1 }}-{{ objective.level.point }}
                                </div>
                              </div>
                            </div>
                            <div class="my-2" v-if="teacher.criterion_marks && teacher.criterion_marks.length">
                              <div v-for="cr in teacher.criterion_marks" :key="cr.id">
                                {{ cr.criterion.letter.toUpperCase() }}. {{ cr.criterion.name }}: <b>{{ cr.mark }}</b>
                              </div>
                            </div>
                            <div class="my-2" v-if="teacher.final_grade_ib">
                              Итоговая оценка IB: <b>{{ teacher.final_grade_ib }}</b>
                            </div>
                            <div class="my-2" v-if="teacher.final_grade">Итоговая оценка: <b>{{ teacher.final_grade }}</b>
                            </div>
                            <div class="my-2 text-muted" v-html="teacher.comment"></div>
                            <hr />
                            <div class="d-flex align-items-center">
                              <i class="bi bi-person"></i>
                              <div class="ms-1">
                                {{ teacher.author.short_name }}
                              </div>
                              <div class="ms-2">
                                {{ formatDate(teacher.updated_at) }}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-else>
                      Репортов не найдено!
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card my-2" v-else>
        <div class="card-body">
          <div class="d-flex justify-content-center">
            Выберите необходимые параметры для отображения карточек студентов
          </div>
        </div>
      </div>
    </div>
    <!-- Подключение модального окна -->
    <confirmation-modal @confirm="removeStudentMentorReport" @cancel="cancelRemoveStudentMentorReport">
      Вы действитель хотите удалить репорт студента:
      <strong>{{ currentStudent.last_name }} {{ currentStudent.first_name }}?</strong>
    </confirmation-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import imageStudent from "@/assets/img/student.svg";

import { formatDate } from "@/common/helpers/date";

import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";

import ReportMentorIbProfile from "@/modules/ReportMentorIbProfile.vue";

import { useGeneralStore } from "@/stores/general";
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";
import { useIboStore } from "@/stores/ibo";


const currentAcademicYear = ref({});
const currentStudyYear = ref({});
const currentReportPeriod = ref({});
const currentGroup = ref({});
const currentStudent = ref({});

const generalStore = useGeneralStore();
const reportStore = useReportStore();
const authStore = useAuthStore();
const iboStore = useIboStore();

const isEditing = ref(false);
let confirmationModal = null;

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

const currentReportType = computed(() => {
  if (currentStudyYear.value.level == 'noo') {
    return { value: 'noo', name: 'Репорт начальной школы' }
  } else {
    return { value: 'ooo', name: 'Репорт средней или старшей школы' }
  }
})

// Фильтр списка периодов репорта по выбранному учебному году
const filteredReportPeriod = computed(() => {
  return reportStore.reportPeriods.filter(
    (item) => item.year.id == currentAcademicYear.value.id
  );
});

// Фильтр списка классов по выбранной параллели
const filteredGroup = computed(() => {
  return generalStore.groups.filter(
    (item) => item.year_study.id == currentStudyYear.value.id
  );
});

// Событие выбора учебного года из выпадающего списка
// запись в localstorage, сброс всех выбранных опций с очисткой списка студентов
const selectAcademicYear = () => {
  localStorage.setItem(
    "selectedAcademicYearReportMentor",
    JSON.stringify(currentAcademicYear.value)
  );
  resetSelectedOptions();
};

// Событие выбора учебной параллели из выпадающего списка:
// запись в localstorage, получение классов, очистка списка студентов, сброс выбранного класса
const selectStudyYear = () => {
  localStorage.setItem(
    "selectedStudyYearReportMentor",
    JSON.stringify(currentStudyYear.value)
  );
  resetSelectedGroup();
  resetStudents();
};

// Событие выбора периода репортов из выпадающего списка:
// запись в localstorage, очистка списка студентов
const selectReportPeriod = () => {
  localStorage.setItem(
    "selectedReportPeriodReportMentor",
    JSON.stringify(currentReportPeriod.value)
  );
  resetStudents();
};

// Событие выбора класса из выпадающего списка
// запись в localstorage, очистка списка студентов
const selectGroup = () => {
  localStorage.setItem(
    "selectedGroupReportMentor",
    JSON.stringify(currentGroup.value)
  );
  resetStudents();
};

// Сброс всех выбранных опций с очисткой списка студентов
const resetSelectedOptions = () => {
  resetSelectedStudyYear();
  resetSelectedReportPeriod();
  resetSelectedGroup();
  resetStudents();
};

// Сброс выбранной учебной параллели
const resetSelectedStudyYear = () => {
  currentStudyYear.value = {};
  localStorage.removeItem("selectedStudyYearReportMentor");
};

// Сброс выбранного периода репрорта
const resetSelectedReportPeriod = () => {
  currentReportPeriod.value = {};
  localStorage.removeItem("selectedReportPeriodReportMentor");
};

// Сброс выбранного класса
const resetSelectedGroup = () => {
  currentGroup.value = {};
  localStorage.removeItem("selectedGroupReportMentor");
};

// Очистка списка студентов
const resetStudents = () => {
  reportStore.studentMentorReports = [];
};

// Запрос на получение списка групп (срабатывает, если выбран текущий учебный год и параллель)
const getGroups = () => {
  if (
    !isEmpty(currentAcademicYear.value)
  ) {
    generalStore.loadGroups({
      params: {
        year_academic: currentAcademicYear.value.id,
      },
    });
  }
};

// Запрос на получение списка студентов
// Нужно выбрать текущий учебный год, параллель и класс
const getStudentMentorReports = () => {
  // console.log('Запрос студентов с репортами')
  if (
    isEmpty(currentStudyYear.value) ||
    isEmpty(currentAcademicYear.value) ||
    isEmpty(currentGroup.value)
  ) {
    return null;
  }
  reportStore
    .loadStudentMentorReports({
      params: {
        groups: 3,
        classes: currentGroup.value.id,
        report_period: currentReportPeriod.value.id,
        report_group: currentGroup.value.id,
      },
    })
    .then(() => {
      console.log(reportStore.studentMentorReports);
    });
};

// Запрос на создание репорта для студента:
// Нужно выбрать период и класс
// После успешного ответа происходит повторный запрос на обновление списка студентов
const createStudentMentorReport = (id) => {
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

// Открытие модального окна для подтверждения удаления
const showConfirmationModal = (student) => {
  currentStudent.value = student;
  confirmationModal.show();
};

// Закрытие модального окна для подтверждения удаления (отмена)
const cancelRemoveStudentMentorReport = () => {
  confirmationModal.hide();
  currentStudent.value = [];
};

// Удаление выбранного репорта студента и закрытие модального окна
// После успешного ответа происходит повторный запрос на обновление списка студентов
const removeStudentMentorReport = () => {
  // console.log('Запрос на удаление репорта студенту: ', currentStudent.value);
  if (currentStudyYear.value.level == "noo") {
    reportStore
      .removeReportMentorPrimary(currentStudent.value.report.id)
      .then((result) => {
        // console.log('Репорт успешно удалён: ', result);
        getStudentMentorReports();
      });
  } else {
    reportStore
      .removeReportMentor(currentStudent.value.report.id)
      .then((result) => {
        // console.log('Репорт успешно удалён: ', result);
        getStudentMentorReports();
      });
  }
  confirmationModal.hide();
};

// Запрос на сохранение данных из компонента редактирования
// После успешного ответа происходит повторный запрос на обновление списка студентов
const handleSave = async (editData, id) => {
  // console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatedObject = {
    id: id,
    [editData.propName]: editData.value,
  };
  if (currentStudyYear.value.level == "noo") {
    reportStore.updateReportMentorPrimary(updatedObject).then((result) => {
      // console.log('Репорт успешно обновлён: ', result)
      getStudentMentorReports();
    });
  } else {
    reportStore.updateReportMentor(updatedObject).then((result) => {
      // console.log('Репорт успешно обновлён: ', result)
      getStudentMentorReports();
    });
  }
};

// Получение состояния режима редактирования в компоненте
// Необходимо для блокирования редактирования других компонентов
const toggleEdit = (state) => {
  isEditing.value = state;
};

// Функция восстановления текущих значений периода, параллели и класса из LocalStorage
const recoveryOptions = () => {
  const savedSelectionStudyYear = JSON.parse(
    localStorage.getItem("selectedStudyYearReportMentor")
  );
  if (savedSelectionStudyYear) {
    currentStudyYear.value = savedSelectionStudyYear;
  }
  const savedSelectionReportPeriod = JSON.parse(
    localStorage.getItem("selectedReportPeriodReportMentor")
  );
  if (savedSelectionReportPeriod) {
    currentReportPeriod.value = savedSelectionReportPeriod;
  }
  const savedSelectionGroup = JSON.parse(
    localStorage.getItem("selectedGroupReportMentor")
  );
  if (savedSelectionGroup) {
    currentGroup.value = savedSelectionGroup;
  }
};

onMounted(() => {
  recoveryOptions();
  if (!generalStore.isAcademicYearsLoaded) {
    generalStore.loadAcademicYears().then(() => {
      currentAcademicYear.value = generalStore.relevantYear;
      getGroups();
      getStudentMentorReports();
    });
  } else {
    currentAcademicYear.value = generalStore.relevantYear;
    getGroups();
    getStudentMentorReports();
  }
  if (!generalStore.isStudyYearsLoaded) {
    generalStore.loadStudyYears();
  }
  if (!reportStore.isReportPeriodsLoaded) {
    reportStore.loadReportPeriods();
  }
  if (!iboStore.isLearnerProfileLoaded) {
    iboStore.loadLearnerProfiles();
  }
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});
</script>

<style scoped>
.list-right-student {
  top: 10px;
}

:target::before {
  content: "";
  display: block;
  height: 90px;
  /* Высота вашей фиксированной шапки */
  margin-top: -90px;
}

:target .card {
  animation: blink 1s ease-in-out 0s 3;
  /* Анимация будет длиться 1 секунду, повторяться 3 раза */
}

@keyframes blink {

  0%,
  100% {
    background-color: transparent;
  }

  50% {
    background-color: rgb(205, 254, 238);
  }

  /* Промежуточный цвет фона для мигания */
}
</style>