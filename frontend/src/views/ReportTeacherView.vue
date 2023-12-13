<template>
  <div>
    <h1>Репорты учителя по предмету</h1>
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
          <simple-dropdown title="Выберите учебный план" v-model="currentCurriculum"
            :propItems="curriculumStore.curriculums" showName="name" @select="selectCurriculum" />
        </div>
      </div>
      <div class="d-flex flex-wrap">
        <div class="m-2">
          <simple-dropdown title="Выберите класс" v-model="currentGroup" :propItems="filteredGroup" showName="full_name"
            :disabled="isEmpty(currentAcademicYear) || isEmpty(currentCurriculum)
              " @select="selectGroup" />
        </div>
        <div class="m-2">
          <search-dropdown title="Выберите предмет" v-model="currentSubject" :propItems="curriculumStore.subjects"
            showName="name" @select="selectSubject" :disabled="isEmpty(currentGroup) || isEmpty(currentCurriculum)" />
        </div>
      </div>
      <button type="button" class="btn btn-primary m-2" @click="getTeacherReports"
        :disabled="isEmpty(currentGroup) || isEmpty(currentReportPeriod) || isEmpty(currentSubject)">
        Показать студентов
      </button>
      <button type="button" class="btn btn-secondary m-2" @click="resetSelectedOptions">
        Сброс
      </button>
      <hr class="hr" />
      <div class="text-bg-light p-2 rounded">
        <h5 v-if="!isEmpty(currentCurriculum)" class="my-2">
          Тип репорта: {{ currentReportType.name }}
        </h5>
        <h5 v-if="!isEmpty(currentSubject)" class="my-2">
          {{ currentSubject.name }}
          <span v-if="currentSubject.group_ib">
            ({{ currentSubject.group_ib.name }}
            {{ currentSubject.group_ib.program.toUpperCase() }})</span>
        </h5>
      </div>
      <!-- Список студентов -->
      <div class="row" v-if="generalStore.users.length">
        <div class="col-md-3">
          <div class="d-flex flex-column align-items-start justify-content-start m-2 list-menu list-right-student">
            <div v-if="!isEmpty(currentGroup)">
              <h5>{{ currentGroup.name }} класс</h5>
              <div v-if="currentGroup.mentor">{{ currentGroup.mentor.short_name }}</div>
              <hr />
            </div>
            <div v-for="user in generalStore.users" :key="user.id">
              <div class="d-flex align-items-center">
                <img :src="user.photo ? user.photo : imageStudent" alt="" width="20" class="me-2 rounded-circle" />
                <div v-if="!checkStudentWithReport(user.id)" class="me-2">
                  {{ user.short_name }}
                </div>
                <a v-else class="select" :href="`#st-${user.id}`">
                  {{ user.short_name }}
                </a>
                <i class="bi bi-plus-square dot-menu" @click="createTeacherReport(user.id)"
                  v-if="!checkStudentWithReport(user.id)"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div v-if="reportStore.reportTeachers.length">
            <div v-for="report in reportStore.reportTeachers" :key="report.id" class="my-3"
              :id="`st-${report.student.id}`">
              <div class="card card-student my-1">
                <div class="card-body d-flex align-items-center">
                  <img :src="report.student.photo ? report.student.photo : imageStudent
                    " alt="" width="50" class="me-2 rounded-circle" />
                  <h4 class="m-0">
                    {{ report.student.last_name }}
                    {{ report.student.first_name }}
                  </h4>
                  <div class="ms-auto">
                    <i class="bi bi-three-dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" href="##" @click="showConfirmationModal(report)">Удалить репорт</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="accordion" :id="`accordionStudent-${report.id}`">
                <div class="accordion-item">
                  <h2 class="accordion-header" :id="`heading-${report.id}`">
                    <button class="accordion-button collapsed p-2"
                      type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${report.id}`"
                      aria-expanded="true" :aria-controls="`collapse-${report.id}`">
                      Репорт учителя по предмету: {{ currentSubject.name }}
                    </button>
                  </h2>
                  <div :id="`collapse-${report.id}`" class="accordion-collapse collapse"
                    :aria-labelledby="`heading-${report.id}`">
                    <div class="accordion-body">
                      <div class="my-3">
                        <report-teacher-myp-strand :report="report" v-if="currentReportType.value == 'ooo'" />
                      </div>
                      <div class="my-3">
                        <report-teacher-myp-criteria :report="report" v-if="currentReportType.value == 'ooo'" />
                      </div>
                      <div class="my-3" v-if="['ooo', 'soo', 'dp'].includes(currentReportType.value)">
                        <div class="d-flex align-items-center">
                          <h5 class="mb-0">Итоговая оценка</h5>
                          <div class="ms-auto">
                            <scale-radio :elementId="String(report.id) + 'grade'" :data="MARK5" :propValue="report.final_grade"
                              propName="final_grade" @save="handleSave($event, report.id)" />
                          </div>
                        </div>
                      </div>
                      <div class="my-3" v-if="currentReportType.value == 'dp'">
                        <div class="d-flex align-items-center">
                          <h5 class="mb-0">Итоговая оценка IB</h5>
                          <div class="ms-auto">
                            <scale-radio :elementId="String(report.id) + 'grade_ib'" :data="MARK7" :propValue="report.final_grade_ib"
                              propName="final_grade_ib" @save="handleSave($event, report.id)" />
                          </div>
                        </div>
                      </div>
                      <div class="my-3">
                        <report-criteria :report="report" typeReport="teacher" v-if="currentReportType.value != 'noo'" />
                      </div>
                      <div class="my-2">
                        <report-teacher-topic :report="report" v-if="currentReportType.value == 'noo'" />
                      </div>
                      <hr />
                      <div class="my-2">
                        <editable-area-tiny class="text-muted" :propData="report.comment" propName="comment"
                          @save="handleSave($event, report.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
                      </div>
                      <hr />
                      <div class="my-2">
                        <event-participation :report="report" />
                      </div>
                      <hr />
                      <div class="d-flex align-items-center">
                        <i class="bi bi-person"></i>
                        <div class="ms-1">{{ report.author.short_name }}</div>
                        <div class="ms-2">
                          {{ formatDate(report.updated_at) }}
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
                Ваших репортов в текущем классе пока нет
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
    <confirmation-modal @confirm="removeTeacherReport" @cancel="cancelRemoveTeacherReport">
      Вы действитель хотите удалить репорт студента?
    </confirmation-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import imageStudent from "@/assets/img/student.svg";
import { MARK5, MARK7, REPORT_TYPES } from "@/common/constants";

import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
import ScaleRadio from "@/common/components/ScaleRadio.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";

import ReportTeacherTopic from "@/modules/ReportTeacherTopic.vue";
import ReportCriteria from "@/modules/ReportCriteria.vue";
import ReportTeacherMypCriteria from "@/modules/ReportTeacherMypCriteria.vue";
import ReportTeacherMypStrand from "@/modules/ReportTeacherMypStrand.vue";
import EventParticipation from "@/modules/EventParticipation.vue";

import { useGeneralStore } from "@/stores/general";
import { useCurriculumStore } from "@/stores/curriculum";
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";
import { useUnitMypStore } from "@/stores/unitMyp";

import { formatDate } from "@/common/helpers/date";

const currentAcademicYear = ref({});
const currentReportPeriod = ref({});
const currentGroup = ref({});
const currentReport = ref({});
const currentSubject = ref({});
const currentCurriculum = ref({});

const generalStore = useGeneralStore();
const reportStore = useReportStore();
const authStore = useAuthStore();
const curriculumStore = useCurriculumStore();
const unitMypStore = useUnitMypStore();

const isEditing = ref(false);
let confirmationModal = null;

const currentReportType = computed(() => {
  const emptyType = { value: null, name: '-' }
  if (currentCurriculum.value.level == 'noo') {
    return REPORT_TYPES.find(i => i.value == 'noo') || emptyType
  } else if (currentCurriculum.value.level == 'ooo') {
    return REPORT_TYPES.find(i => i.value == 'ooo') || emptyType
  } else if (currentCurriculum.value.level == 'soo' && currentCurriculum.value.ib == true) {
    return REPORT_TYPES.find(i => i.value == 'dp') || emptyType
  } else if (currentCurriculum.value.level == 'soo' && currentCurriculum.value.ib == false) {
    return REPORT_TYPES.find(i => i.value == 'soo') || emptyType
  } else {
    return emptyType
  }
})

// Проверка на наличие репорта у студента с текущим ID
const checkStudentWithReport = (id) => {
  return reportStore.reportTeachers.some((item) => item.student.id == id);
};

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

// Фильтр списка периодов репорта по выбранному учебному году
const filteredReportPeriod = computed(() => {
  return reportStore.reportPeriods.filter(
    (item) => item.year.id == currentAcademicYear.value.id
  );
});

// Фильтр списка классов по выбранному учебному плану
const filteredGroup = computed(() => {
  return generalStore.groups.filter(
    (item) => item.curriculum == currentCurriculum.value.id
  );
});

// Событие выбора учебного года из выпадающего списка
// запись в localstorage, сброс всех выбранных опций с очисткой списка студентов
const selectAcademicYear = () => {
  localStorage.setItem(
    "selectedAcademicYearReportTeacher",
    JSON.stringify(currentAcademicYear.value)
  );
  resetSelectedOptions();
};

// Событие выбора периода репортов из выпадающего списка:
// запись в localstorage, очистка списка студентов
const selectReportPeriod = () => {
  localStorage.setItem(
    "selectedReportPeriodReportTeacher",
    JSON.stringify(currentReportPeriod.value)
  );
  resetStudents();
};

// Событие выбора учебного плана из выпадающего списка:
// запись в localstorage, очистка списка студентов
const selectCurriculum = () => {
  localStorage.setItem(
    "selectedCurriculumReportTeacher",
    JSON.stringify(currentCurriculum.value)
  );
  resetSelectedGroup();
  resetSelectedSubject();
  resetStudents();
  getSubjects();
};

// Событие выбора класса из выпадающего списка
// запись в localstorage, очистка списка студентов
const selectGroup = () => {
  localStorage.setItem(
    "selectedGroupReportTeacher",
    JSON.stringify(currentGroup.value)
  );
  resetSelectedSubject();
  resetStudents();
  getSubjects();
};

// Событие выбора предмета из выпадающего списка
// запись в localstorage, очистка списка студентов
const selectSubject = () => {
  localStorage.setItem(
    "selectedSubjectReportTeacher",
    JSON.stringify(currentSubject.value)
  );
  resetStudents();
  getObjective();
  getStrands();
};

// Сброс всех выбранных опций с очисткой списка студентов
const resetSelectedOptions = () => {
  resetSelectedReportPeriod();
  resetSelectedCurriculum();
  resetSelectedGroup();
  resetSelectedSubject();
  resetStudents();
};

// Сброс выбранного периода репрорта
const resetSelectedReportPeriod = () => {
  currentReportPeriod.value = {};
  localStorage.removeItem("selectedReportPeriodReportTeacher");
};

// Сброс выбранного учебного плана
const resetSelectedCurriculum = () => {
  currentCurriculum.value = {};
  localStorage.removeItem("selectedCurriculumReportTeacher");
};

// Сброс выбранного класса
const resetSelectedGroup = () => {
  currentGroup.value = {};
  localStorage.removeItem("selectedGroupReportTeacher");
};

// Сброс выбранного предмета
const resetSelectedSubject = () => {
  currentSubject.value = {};
  localStorage.removeItem("selectedSubjectReportTeacher");
};

// Очистка списка студентов
const resetStudents = () => {
  reportStore.reportTeachers = [];
  generalStore.users = [];
};

// Запрос на получение списка групп (срабатывает, если выбран текущий учебный год и параллель)
const getGroups = () => {
  if (!isEmpty(currentAcademicYear.value)) {
    generalStore.loadGroups({
      params: {
        year_academic: currentAcademicYear.value.id,
      },
    });
  }
};

// Запрос на получение списка учебных планов (срабатывает, если выбран текущий учебный год)
const getCurriculums = () => {
  if (!isEmpty(currentAcademicYear.value)) {
    curriculumStore.loadCurriculums({
      params: {
        year: currentAcademicYear.value.id,
      },
    });
  }
};

// Запрос на получение списка учебных планов (срабатывает, если выбран учебный план и групппа)
const getSubjects = () => {
  if (!(isEmpty(currentCurriculum.value) && isEmpty(currentGroup.value))) {
    curriculumStore.loadSubjects({
      params: {
        curriculum_loads__curriculum: currentCurriculum.value.id,
        curriculum_loads__years__classes: currentGroup.value.id,
      },
    });
  }
};

const getStudents = () => {
  // console.log('Запрос студентов')
  if (!isEmpty(currentGroup.value)) {
    generalStore.loadUsers({
      params: {
        groups: 3,
        classes: currentGroup.value.id,
      },
    });
  }
};

// Запрос на получение списка студентов
// Нужно выбрать текущий учебный год, параллель и класс
const getTeacherReports = () => {
  // console.log('Запрос репортов')
  if (
    !(
      isEmpty(currentCurriculum.value) &&
      isEmpty(currentAcademicYear.value) &&
      isEmpty(currentGroup.value)
    )
  ) {
    const config = {
      params: {
        group: currentGroup.value.id,
        period: currentReportPeriod.value.id,
        subject: currentSubject.value.id,
        event_group: currentGroup.value.id,
      },
    };
    if (currentCurriculum.value.level == "noo") {
      reportStore.loadReportTeachersPrimary(config).then(() => {
        // console.log(reportStore.reportTeachers);
      });
    } else if (currentCurriculum.value.level == "ooo") {
      reportStore.loadReportTeachersSecondary(config).then(() => {
        // console.log(reportStore.reportTeachers);
      });
    } else if (currentCurriculum.value.level == "soo") {
      reportStore.loadReportTeachersHigh(config).then(() => {
        // console.log(reportStore.reportTeachers);
      });
    } else {
      // console.log('Не выбран уровень')
    }
    getStudents();
  }
};

// Запрос на создание репорта для студента:
// Нужно выбрать период и класс
// После успешного ответа происходит повторный запрос на обновление списка студентов
const createTeacherReport = (id) => {
  if (isEmpty(currentReportPeriod.value) || isEmpty(currentGroup.value)) {
    return null;
  }
  const data = {
    student: id,
    author: authStore.user.id,
    period: currentReportPeriod.value.id,
    group: currentGroup.value.id,
    subject: currentSubject.value.id,
  };
  if (currentCurriculum.value.level == "noo") {
    // console.log('Запрос на создание репорта для студента начальной школы')
    reportStore.createReportTeacherPrimary(data).then((result) => {
      // console.log('Репорт начальной школы успешно добавлен: ', result)
      getTeacherReports();
    });
  } else if (currentCurriculum.value.level == "ooo") {
    // console.log('Запрос на создание репорта для студента средней школы')
    reportStore.createReportTeacherSecondary(data).then((result) => {
      // console.log('Репорт средней школы успешно добавлен: ', result)
      getTeacherReports();
    });
  } else if (currentCurriculum.value.level == "soo") {
    // console.log('Запрос на создание репорта для студента старшей школы')
    reportStore.createReportTeacherHigh(data).then((result) => {
      // console.log('Репорт старшей школы успешно добавлен: ', result)
      getTeacherReports();
    });
  } else {
    // console.log('Не выбран уровень')
  }
};

// Открытие модального окна для подтверждения удаления
const showConfirmationModal = (student) => {
  currentReport.value = student;
  confirmationModal.show();
};

// Закрытие модального окна для подтверждения удаления (отмена)
const cancelRemoveTeacherReport = () => {
  confirmationModal.hide();
  currentReport.value = [];
};

// Удаление выбранного репорта студента и закрытие модального окна
// После успешного ответа происходит повторный запрос на обновление списка студентов
const removeTeacherReport = () => {
  // console.log('Запрос на удаление репорта студенту: ', currentReport.value);
  const id = currentReport.value.id;
  if (currentCurriculum.value.level == "noo") {
    // console.log('Запрос на удаление репорта для студента начальной школы')
    reportStore.removeReportTeacherPrimary(id).then((result) => {
      // console.log('Репорт начальной школы успешно удалён: ', result)
      getTeacherReports();
    });
  } else if (currentCurriculum.value.level == "ooo") {
    // console.log('Запрос на удаление репорта для студента средней школы')
    reportStore.removeReportTeacherSecondary(id).then((result) => {
      // console.log('Репорт средней школы успешно удалён: ', result)
      getTeacherReports();
    });
  } else if (currentCurriculum.value.level == "soo") {
    // console.log('Запрос на удаление репорта для студента старшей школы')
    reportStore.removeReportTeacherHigh(id).then((result) => {
      // console.log('Репорт старшей школы успешно удалён: ', result)
      getTeacherReports();
    });
  } else {
    // console.log('Не выбран уровень')
  }
  confirmationModal.hide();
};

// Получение состояния режима редактирования в компоненте
// Необходимо для блокирования редактирования других компонентов
const toggleEdit = (state) => {
  isEditing.value = state;
};

// Замена обновлённого репорта учителя
const replaceReportTeacher = (data) => {
  // console.log("Репорт успешно обновлён: ", data);
  const index = reportStore.reportTeachers.findIndex(
    (item) => item.id === data.id
  );
  if (index != -1) {
    reportStore.reportTeachers[index] = data;
  }
};

// Запрос на сохранение данных из компонента редактирования
// После успешного ответа происходит повторный запрос на обновление списка студентов
const handleSave = async (editData, id) => {
  // console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  };
  if (currentCurriculum.value.level == "noo") {
    // console.log('Запрос на удаление репорта для студента начальной школы')
    reportStore.updateReportTeacherPrimary(updatingData).then((result) => {
      replaceReportTeacher(result.data);
    });
  } else if (currentCurriculum.value.level == "ooo") {
    // console.log('Запрос на удаление репорта для студента средней школы')
    reportStore.updateReportTeacherSecondary(updatingData).then((result) => {
      replaceReportTeacher(result.data);
    });
  } else if (currentCurriculum.value.level == "soo") {
    // console.log('Запрос на удаление репорта для студента старшей школы')
    reportStore.updateReportTeacherHigh(updatingData).then((result) => {
      replaceReportTeacher(result.data);
    });
  } else {
    // console.log('Не выбран уровень')
  }
};

// Функция восстановления текущих значений периода, параллели и класса из LocalStorage
const recoveryOptions = () => {
  const savedSelectionReportPeriod = JSON.parse(
    localStorage.getItem("selectedReportPeriodReportTeacher")
  );
  if (savedSelectionReportPeriod) {
    currentReportPeriod.value = savedSelectionReportPeriod;
  }
  const savedSelectionCurriculum = JSON.parse(
    localStorage.getItem("selectedCurriculumReportTeacher")
  );
  if (savedSelectionCurriculum) {
    currentCurriculum.value = savedSelectionCurriculum;
  }
  const savedSelectionGroup = JSON.parse(
    localStorage.getItem("selectedGroupReportTeacher")
  );
  if (savedSelectionGroup) {
    currentGroup.value = savedSelectionGroup;
  }
  const savedSelectionSubject = JSON.parse(
    localStorage.getItem("selectedSubjectReportTeacher")
  );
  if (savedSelectionSubject) {
    currentSubject.value = savedSelectionSubject;
  }
};

const getStrands = () => {
  if (currentReportType.value.value == 'ooo' && currentSubject.value.group_ib) {
    unitMypStore.loadStrands({
      params: {
        objective__group: currentSubject.value.group_ib.id
      }
    });
  }
}

const getObjective = () => {
  if (currentReportType.value.value == 'ooo') {
    unitMypStore.loadObjectives().then(() => {
      getStrands();
    });
  }
}

// Запросы и установки при монтировании компонента:
// Восстановление опций из LocalStorage, загрузка данных в соответствии с опциями (если они не загружены)
// Создание объекта модального окна из компонента
onMounted(() => {
  recoveryOptions();
  if (!generalStore.isAcademicYearsLoaded) {
    generalStore.loadAcademicYears().then(() => {
      currentAcademicYear.value = generalStore.relevantYear;
      getGroups();
      getCurriculums();
    });
  } else {
    currentAcademicYear.value = generalStore.relevantYear;
    getGroups();
    getCurriculums();
  }
  if (!reportStore.isReportPeriodsLoaded) {
    reportStore.loadReportPeriods();
  }
  if (!generalStore.isGroupsLoaded) {
  }
  getSubjects();
  getObjective();
  getStrands();
  getTeacherReports();
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});
</script>

<style scoped>
.list-menu {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
}

.report-success {
  background-color: rgb(174, 232, 232);
}

.select {
  font-weight: bold;
}

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

:target .card-student {
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