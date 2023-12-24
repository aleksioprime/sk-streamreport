<template>
  <div>
    <h1>Репорты учителя по предмету</h1>
    <div class="py-2">
      <transition>
        <div v-if="isLoadedFilters">
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
              <search-dropdown
                :title="curriculumStore.subjects.length ? 'Выберите предмет' : 'Добавьте предметы выбранного класса в нагрузку'"
                v-model="currentSubject" :propItems="curriculumStore.subjects" showName="name" @select="selectSubject"
                :disabled="isEmpty(currentGroup) || !curriculumStore.subjects.length" />
            </div>
          </div>
          <div class="d-flex flex-wrap">
            <div class="m-2">
              <group-classes :propItems="generalStore.groups" v-model="currentGroup"
                :disabled="isEmpty(currentAcademicYear)" @select="selectGroup" />
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
          <!-- <div class="text-bg-light p-2 rounded">
          <h5 v-if="!isEmpty(currentGroup)" class="my-2">
            Тип репорта: {{ currentReportType.name }}
          </h5>
          <h5 v-if="!isEmpty(currentSubject)" class="my-2">
            {{ currentSubject.name }}
            <span v-if="currentSubject.group_ib">
              ({{ currentSubject.group_ib.name }}
              {{ currentSubject.group_ib.program.toUpperCase() }})</span>
          </h5>
        </div> -->
        </div>
      </transition>
      <div v-if="reportStore.studentExtraReports.length || isLoadedFilters">
        <transition>
          <div class="row" v-if="generalStore.users.length">
            <!-- Список студентов -->
            <div class="col-md-auto">
              <div
                class="d-flex flex-column align-items-start justify-content-start m-2 list-menu list-right-student pb-3">
                <div v-if="!isEmpty(currentGroup)">
                  <h5>{{ currentGroup.name }} класс</h5>
                  <div v-if="currentGroup.mentor">{{ currentGroup.mentor.short_name }}</div>
                  <hr />
                </div>
                <div class="d-flex flex-md-column flex-wrap flex-md-nowrap">
                  <div v-for="user in generalStore.users" :key="user.id">
                    <div class="d-flex align-items-center me-2">
                      <img :src="user.photo ? user.photo : imageStudent" alt="" width="20" class="me-2 rounded-circle" />
                      <div class="flex-shrink-0">
                        <div v-if="!checkStudentWithReport(user.id)" class="me-2">
                          {{ user.short_name }}
                        </div>
                        <a v-else class="select"
                          :class="{ 'select-teacher': !isAuthor(reportStore.reportTeachers.find((item) => item.student.id == user.id)) }"
                          :href="`#st-${user.id}`">
                          {{ user.short_name }}
                        </a>
                      </div>
                      <div class="ms-auto" v-if="isTeacher()">
                        <i class="bi bi-plus-square dot-menu" @click="createTeacherReport(user.id)"
                          v-if="!checkStudentWithReport(user.id)"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Список репортов -->
            <div class="col">
              <div class="loader-spin" v-if="isLoadedReport"></div>
              <div v-if="reportStore.reportTeachers.length">
                <transition-group name="card">
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
                        <div class="ms-auto" v-if="isAuthor(report)">
                          <i class="bi bi-three-dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
                          <ul class="dropdown-menu">
                            <li>
                              <a class="dropdown-item" href="javascript:void(0)"
                                @click.prevent="showConfirmationModal(report)">Удалить репорт</a>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                    <div class="accordion" :id="`accordionStudent-${report.id}`">
                      <div class="accordion-item">
                        <h2 class="accordion-header" :id="`heading-${report.id}`">
                          <button class="accordion-button collapsed p-2"
                            :class="{ 'report-complete': checkReportComplete(report) }" type="button"
                            data-bs-toggle="collapse" :data-bs-target="`#collapse-${report.id}`" aria-expanded="true"
                            :aria-controls="`collapse-${report.id}`">
                            Репорт учителя по предмету: {{ currentSubject.name }}
                          </button>
                        </h2>
                        <div :id="`collapse-${report.id}`" class="accordion-collapse collapse"
                          :aria-labelledby="`heading-${report.id}`">
                          <div class="accordion-body">
                            <div class="my-1 d-flex align-items-center">
                              <div class="me-2"><b>Дополнительный предмет:</b></div>
                              <search-dropdown-multiple class="my-2" title="Не выбрано" v-model="report.extra_subjects"
                                :propItems="curriculumStore.subjects" showName="name" propName="extra_subjects"
                                @select="handleSave($event, report.id)" :disabled="!isAuthor(report)" />
                            </div>
                            <div class="my-3">
                              <report-teacher-myp-strand :report="report" v-if="currentReportType.value == 'ooo'"
                                :allowedMode="isAuthor(report)" />
                            </div>
                            <div class="my-3">
                              <report-teacher-myp-criteria :report="report" v-if="currentReportType.value == 'ooo'"
                                :allowedMode="isAuthor(report)" />
                            </div>
                            <div class="my-3" v-if="['ooo', 'soo', 'dp'].includes(currentReportType.value)">
                              <div class="d-flex align-items-center">
                                <h5 class="mb-0">Итоговая оценка</h5>
                                <div class="ms-auto" v-if="isAuthor(report)">
                                  <scale-radio :elementId="String(report.id) + 'grade'" :data="MARK5"
                                    :propValue="report.final_grade" propName="final_grade"
                                    @save="handleSave($event, report.id)" />
                                </div>
                                <div v-else class="ms-auto">{{ report.final_grade || 'Нет оценки' }}</div>
                              </div>
                            </div>
                            <div class="my-3" v-if="currentReportType.value == 'dp'">
                              <div class="d-flex align-items-center">
                                <h5 class="mb-0">Итоговая оценка IB</h5>
                                <div class="ms-auto" v-if="isAuthor(report)">
                                  <scale-radio :elementId="String(report.id) + 'grade_ib'" :data="MARK7"
                                    :propValue="report.final_grade_ib" propName="final_grade_ib"
                                    @save="handleSave($event, report.id)" />
                                </div>
                                <div v-else class="ms-auto">{{ report.final_grade_ib }}</div>
                              </div>
                            </div>
                            <div class="my-3">
                              <report-criteria :report="report" typeReport="teacher"
                                v-if="currentReportType.value != 'noo'" :allowedMode="isAuthor(report)" />
                            </div>
                            <div class="my-2">
                              <report-teacher-topic :report="report" v-if="currentReportType.value == 'noo'"
                                :allowedMode="isAuthor(report)" />
                            </div>
                            <hr />
                            <div class="my-2">
                              <editable-area-tiny class="text-muted" :propData="report.comment" propName="comment"
                                @save="handleSave($event, report.id)" :isEditing="isEditing" @toggleEdit="toggleEdit"
                                :allowedMode="isAuthor(report)" />
                            </div>
                            <hr />
                            <div class="my-2">
                              <event-participation :report="report" :allowedMode="isAuthor(report)" />
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
                </transition-group>
              </div>
              <div class="card my-2" v-else>
                <div class="card-body">
                  <div class="d-flex justify-content-center">
                    Репортов в текущем классе пока нет
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
        </transition>
      </div>
      <!-- <div v-else>
        <div class="alert alert-danger" role="alert">
          Ошибка! Данные не обнаружены
        </div>
      </div> -->
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

import SearchDropdownMultiple from "@/common/components/SearchDropdownMultiple.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
import ScaleRadio from "@/common/components/ScaleRadio.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";

import GroupClasses from "@/modules/GroupClasses.vue";
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

const generalStore = useGeneralStore();
const reportStore = useReportStore();
const authStore = useAuthStore();
const curriculumStore = useCurriculumStore();
const unitMypStore = useUnitMypStore();

const isEditing = ref(false);
let confirmationModal = null;
const isLoadedReport = ref(false);

const currentReportType = computed(() => {
  const emptyType = { value: null, name: '-' }
  if (isEmpty(currentGroup.value)) {
    return emptyType
  }
  if (currentGroup.value.curriculum.level == 'noo') {
    return REPORT_TYPES.find(i => i.value == 'noo') || emptyType
  } else if (currentGroup.value.curriculum.level == 'ooo') {
    return REPORT_TYPES.find(i => i.value == 'ooo') || emptyType
  } else if (currentGroup.value.curriculum.level == 'soo' && currentGroup.value.curriculum.ib == true) {
    return REPORT_TYPES.find(i => i.value == 'dp') || emptyType
  } else if (currentGroup.value.curriculum.level == 'soo' && currentGroup.value.curriculum.ib == false) {
    return REPORT_TYPES.find(i => i.value == 'soo') || emptyType
  } else {
    return emptyType
  }
})

const isLoadedFilters = computed(() => {
  return reportStore.reportPeriods.length && generalStore.groups.length && generalStore.academicYears.length
})

// Вспомогательная функция для проверки разрешения редактирования только автору
const isAuthor = (report) => {
  if (authStore.user) {
    return !report || report && report.author.id == authStore.user.id
  }
  return false
}

// Вспомогательная функция для проверки разрешения редактирования только учителю
const isTeacher = () => {
  if (authStore.user) {
    return authStore.user.teaching_loads.some(item => item.subject.id == currentSubject.value.id && item.groups.map(i => i.id).includes(currentGroup.value.id))
  }
  return false
}

// Проверка на наличие репорта у студента с текущим ID
const checkStudentWithReport = (id) => {
  return reportStore.reportTeachers.some((item) => item.student.id == id);
};

function isPropertyFilledInEveryObject(array, propertyName) {
  return array.every(obj => obj[propertyName] !== undefined && obj[propertyName] !== null && obj[propertyName] !== '');
}

const checkReportComplete = (report) => {
  if (currentReportType.value.value == 'noo') {
    return report.comment && report.topic_achievements.length && isPropertyFilledInEveryObject(report.topic_achievements, 'level')
  } else if (currentReportType.value.value == 'ooo') {
    return report.comment && report.final_grade && report.criterion_marks.length && isPropertyFilledInEveryObject(report.criterion_marks, 'mark')
  } else if (currentReportType.value.value == 'soo') {
    return report.comment && report.final_grade
  } else if (currentReportType.value.value == 'dp') {
    return report.comment && report.final_grade && report.final_grade_ib
  } else {
    return report.comment
  }
}

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).length === 0;
  }
  return true
};

// Фильтр списка периодов репорта по выбранному учебному году
const filteredReportPeriod = computed(() => {
  return reportStore.reportPeriods.filter(
    (item) => item.year.id == currentAcademicYear.value.id
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

// Событие выбора класса из выпадающего списка
// запись в localstorage, очистка списка студентов
const selectGroup = () => {
  localStorage.setItem(
    "selectedGroupReportTeacher",
    JSON.stringify(currentGroup.value)
  );
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
  resetSelectedGroup();
  resetSelectedSubject();
  resetStudents();
};

// Сброс выбранного периода репрорта
const resetSelectedReportPeriod = () => {
  currentReportPeriod.value = {};
  localStorage.removeItem("selectedReportPeriodReportTeacher");
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

// Запрос на получение списка учебных планов (срабатывает, если выбран учебный план и групппа)
const getSubjects = () => {
  if (!isEmpty(currentGroup.value)) {
    let config = {
      params: {
        curriculum_loads__years__classes: currentGroup.value.id,
      }
    }
    if (!authStore.isAdmin) {
      config.params.teaching_loads__teacher = authStore.user.id;
      config.params.teaching_loads__groups = [...new Set(authStore.user.teaching_loads.flatMap(obj => obj.groups.map(group => group.id)))];
    }
    curriculumStore.loadSubjects(config).then((result) => {
      if (!curriculumStore.subjects.map(i => i.id).includes(currentSubject.value.id))
        resetSelectedSubject();
    });
  }
};

const getStudents = () => {
  // console.log('Запрос студентов')
  if (!isEmpty(currentGroup.value)) {
    generalStore.loadUsers({
      params: {
        groups: [3],
        classes: currentGroup.value.id,
      },
    });
  }
};

// Запрос на получение списка студентов
// Нужно выбрать текущий учебный год, параллель и класс
const getTeacherReports = async () => {
  // console.log('Запрос репортов')
  if (
    !isEmpty(currentAcademicYear.value) &&
    !isEmpty(currentGroup.value) &&
    !isEmpty(currentSubject.value)
  ) {
    isLoadedReport.value = true;
    const config = {
      params: {
        group: currentGroup.value.id,
        period: currentReportPeriod.value.id,
        subject: currentSubject.value.id,
        event_group: currentGroup.value.id,
      },
    };
    if (currentGroup.value.year_study.level == "noo") {
      await reportStore.loadReportTeachersPrimary(config);
    } else if (currentGroup.value.year_study.level == "ooo") {
      await reportStore.loadReportTeachersSecondary(config);
    } else if (currentGroup.value.year_study.level == "soo") {
      await reportStore.loadReportTeachersHigh(config);
    } else {
      console.log('Не выбран уровень')
    }
    isLoadedReport.value = false;
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
  if (currentGroup.value.year_study.level == "noo") {
    // console.log('Запрос на создание репорта для студента начальной школы')
    reportStore.createReportTeacherPrimary(data).then((result) => {
      // console.log('Репорт начальной школы успешно добавлен: ', result)
      authStore.showMessageSuccess('Репорт учителя начальной школы добавлен');
      getTeacherReports();
    });
  } else if (currentGroup.value.year_study.level == "ooo") {
    // console.log('Запрос на создание репорта для студента средней школы')
    reportStore.createReportTeacherSecondary(data).then((result) => {
      // console.log('Репорт средней школы успешно добавлен: ', result)
      authStore.showMessageSuccess('Репорт учителя средней школы добавлен');
      getTeacherReports();
    });
  } else if (currentGroup.value.year_study.level == "soo") {
    // console.log('Запрос на создание репорта для студента старшей школы')
    reportStore.createReportTeacherHigh(data).then((result) => {
      // console.log('Репорт старшей школы успешно добавлен: ', result)
      authStore.showMessageSuccess('Репорт учителя старшей школы добавлен');
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
  if (currentGroup.value.year_study.level == "noo") {
    // console.log('Запрос на удаление репорта для студента начальной школы')
    reportStore.removeReportTeacherPrimary(id).then((result) => {
      authStore.showMessageSuccess('Репорт учителя начальной школы удалён');
      getTeacherReports();
    });
  } else if (currentGroup.value.year_study.level == "ooo") {
    // console.log('Запрос на удаление репорта для студента средней школы')
    reportStore.removeReportTeacherSecondary(id).then((result) => {
      authStore.showMessageSuccess('Репорт учителя средней школы удалён');
      getTeacherReports();
    });
  } else if (currentGroup.value.year_study.level == "soo") {
    // console.log('Запрос на удаление репорта для студента старшей школы')
    reportStore.removeReportTeacherHigh(id).then((result) => {
      // console.log('Репорт старшей школы успешно удалён: ', result)
      authStore.showMessageSuccess('Репорт учителя старшей школы удалён');
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
  console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  };
  if (currentGroup.value.year_study.level == "noo") {
    reportStore.updateReportTeacherPrimary(updatingData).then((result) => {
      authStore.showMessageSuccess('Сохранено');
      replaceReportTeacher(result.data);
    });
  } else if (currentGroup.value.year_study.level == "ooo") {
    reportStore.updateReportTeacherSecondary(updatingData).then((result) => {
      authStore.showMessageSuccess('Сохранено');
      replaceReportTeacher(result.data);
    });
  } else if (currentGroup.value.year_study.level == "soo") {
    reportStore.updateReportTeacherHigh(updatingData).then((result) => {
      authStore.showMessageSuccess('Сохранено');
      replaceReportTeacher(result.data);
    });
  } else {
    console.log('Не определён уровень')
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
onMounted(async () => {
  generalStore.users = [];
  recoveryOptions();
  if (!generalStore.isAcademicYearsLoaded) {
    await generalStore.loadAcademicYears()
  }
  currentAcademicYear.value = generalStore.relevantYear;
  getGroups();
  reportStore.loadReportPeriods();
  getSubjects();
  getObjective();
  getStrands();
  getTeacherReports();
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});
</script>

<style scoped>
.report-complete {
  background-color: #b0e4af;
}

.list-menu {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
}

.report-success {
  background-color: var(--bs-secondary);
}

.select {
  font-weight: bold;
}

.select-teacher {
  color: grey !important;
}

.list-right-student {
  top: 10px;
  max-height: 100vh;
  overflow-y: scroll;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.list-right-student::-webkit-scrollbar {
  display: none;
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
    background-color: #59C5C5;
  }

  /* Промежуточный цвет фона для мигания */
}

.v-enter-active {
  transition: opacity 0.5s ease;
}

.v-enter-from {
  opacity: 0;
}

.card-enter-active,
.card-leave-active {
  transition: all 0.5s ease;
}

.card-enter-from,
.card-leave-to {
  opacity: 0;
  transform: translateY(30px);
}</style>