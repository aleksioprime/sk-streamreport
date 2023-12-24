<template>
  <div>
    <h1>Репорты руководителя класса</h1>
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
          <button type="button" class="btn btn-secondary m-2" @click="resetSelectedOptions">
            Сброс
          </button>
        </div>
        <div class="d-flex flex-wrap">
          <div class="m-2">
            <group-classes :propItems="generalStore.groups" v-model="currentGroup" :disabled="isEmpty(currentAcademicYear)" @select="selectGroup"/>
          </div>
        </div>
        <button type="button" class="btn btn-primary m-2" @click="getStudentMentorReports"
          :disabled="isEmpty(currentGroup) || isEmpty(currentReportPeriod)">
          Показать студентов
        </button>
        <hr class="hr" />
      <!-- <div class="text-bg-light p-2 rounded">
        <h5 v-if="!isEmpty(currentGroup)" class="mb-2">
          Тип репорта: {{ currentReportType.name }}
        </h5>
      </div> -->
      </div>
      </transition>
      <transition>
      <div v-if="reportStore.studentMentorReports.length" class="row">
        <div class="col-md-auto">
          <div class="d-flex flex-column align-items-start justify-content-start m-2 sticky-top list-right-student pb-3">
            <div v-if="!isEmpty(currentGroup)">
              <h5>{{ currentGroup.name }} класс</h5>
              <div v-if="currentGroup.mentor">{{ currentGroup.mentor.short_name }}</div>
              <hr />
            </div>
            <div class="d-flex flex-md-column flex-wrap flex-md-nowrap">
              <div v-for="student in reportStore.studentMentorReports" :key="student.id">
                <div class="d-flex align-items-center my-1 me-2">
                  <img :src="student.photo ? student.photo : imageStudent" alt="" width="20"
                    class="me-2 rounded-circle" />
                  <a class="select" :href="`#st-${student.id}`" :class="{'no-report': !student.report }">
                    {{ student.short_name }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col pe-3">  
          <div v-for="student in reportStore.studentMentorReports" :key="student.id" class="my-3"
            :id="`st-${student.id}`">
            <div class="card card-student my-1 anchor-student">
              <div class="card-body d-flex align-items-center ">
                <img :src="student.photo ? student.photo : imageStudent" alt="" width="50" class="me-2 rounded-circle" />
                <h4 class="m-0">
                  {{ student.last_name }} {{ student.first_name }}
                </h4>
                <div class="ms-auto">
                  <i class="bi bi-file-earmark-word dot-menu" @click="exportReportToWord(student)"
                    v-if="student.report"></i>
                </div>
                <div class="ms-2" v-if="isMentor()">
                  <i class="bi bi-three-dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"
                    v-if="isAuthor(student.report)"></i>
                  <ul class="dropdown-menu">
                    <li v-if="!student.report">
                      <a class="dropdown-item" href="javascript:void(0)"
                        @click.prevent="createStudentMentorReport(student.id)">Добавить репорт
                        руководителя</a>
                    </li>
                    <li v-else>
                      <a class="dropdown-item" href="javascript:void(0)"
                        @click.prevent="showConfirmationModal(student)">Удалить репорт
                        руководителя</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <transition name="card">
            <div class="accordion my-1" :id="`accordionStudent-${student.id}`" v-if="student.report">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`heading-${student.id}`">
                  <button class="accordion-button collapsed p-2" :class="{ 'report-complete': checkReportComplete(student.report) }"
                    type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${student.id}`"
                    aria-expanded="true" :aria-controls="`collapse-${student.id}`">
                    Репорт руководителя класса
                  </button>
                </h2>
                <div :id="`collapse-${student.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`heading-${student.id}`">
                  <div class="accordion-body">
                    <div class="my-2">
                      <report-mentor-ib-profile :report="student.report" v-if="currentGroup.curriculum && currentGroup.curriculum.level == 'noo'"
                        :allowedMode="isAuthor(student.report)" />
                    </div>
                    <div class="my-2">
                      <report-mentor-primary-unit :report="student.report" v-if="currentGroup.curriculum && currentGroup.curriculum.level == 'noo'"
                        :allowedMode="isAuthor(student.report)" />
                    </div>
                    <hr />
                    <div class="my-2">
                      <editable-area-tiny class="text-muted" :propData="student.report.comment" propName="comment"
                        @save="handleSave($event, student.report.id)" :isEditing="isEditing" @toggleEdit="toggleEdit"
                        :allowedMode="isAuthor(student.report)" />
                    </div>
                    <hr />
                    <div class="my-2">
                      <event-participation :report="student.report" :allowedMode="isAuthor(student.report)" />
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
            </transition>
            <div class="accordion my-1" :id="`accordionStudentExtra-${student.id}`" v-if="student.report_extras.length">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`headingExtra-${student.id}`">
                  <button class="accordion-button collapsed p-2" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#collapseExtra-${student.id}`" aria-expanded="true"
                    :aria-controls="`collapseExtra-${student.id}`">
                    Репорты службы сопровождения
                  </button>
                </h2>
                <div :id="`collapseExtra-${student.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`headingExtra-${student.id}`">
                  <div class="accordion-body">
                    <div v-if="student.report_extras.length">
                      <div v-for="extra in student.report_extras" :key="extra.id" class="card card-body my-2">
                        <div>
                          <div class="my-2"><b>{{ extra.role }}</b></div>
                          <div class="my-2">Результаты по критериям</div>
                          <table class="table table-sm table-bordered">
                            <thead>
                              <tr>
                                <th scope="col" style="width: 100%;">Критерий</th>
                                <th scope="col" style="min-width: 120px;">Результат</th>
                              </tr>
                            </thead>
                            <tbody>
                              <template v-for="achievement in extra.criterion_achievements" :key="achievement.id">
                                <tr>
                                  <td>
                                    <span class="me-2">{{ achievement.criterion_name }}</span>
                                  </td>
                                  <td>
                                    <span class="me-2">{{ achievement.achievement_name }}</span>
                                  </td>
                                </tr>
                                <tr v-if="achievement.achievement_description">
                                  <td colspan="2">
                                    <div>{{ achievement.achievement_description }}</div>
                                  </td>
                                </tr>
                              </template>
                            </tbody>
                          </table>
                        </div>
                        <hr />
                        <div class="my-2" v-html="extra.comment" v-if="extra.comment"></div>
                        <div v-else>Нет информации</div>
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
                    <div v-else cla>
                      Репортов не найдено!
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="accordion my-1" :id="`accordionStudentTeacher-${student.id}`"
              v-if="student.report_teachers.length">
              <div class="accordion-item">
                <h2 class="accordion-header" :id="`headingTeacher-${student.id}`">
                  <button class="accordion-button collapsed p-2" type="button" data-bs-toggle="collapse"
                    :data-bs-target="`#collapseTeacher-${student.id}`" aria-expanded="true"
                    :aria-controls="`collapseTeacher-${student.id}`">
                    Репорты учителей
                  </button>
                </h2>
                <div :id="`collapseTeacher-${student.id}`" class="accordion-collapse collapse"
                  :aria-labelledby="`headingTeacher-${student.id}`">
                  <div class="accordion-body">
                    <div v-if="student.report_teachers && student.report_teachers.length">
                      <div v-for="teacher in student.report_teachers" :key="teacher.id" class="my-2">
                        <div class="accordion" :id="`accordionTeacher-${student.id}-${teacher.id}`">
                          <div class="accordion-item">
                            <h2 class="accordion-header">
                              <button class="accordion-button p-2 collapsed" type="button" data-bs-toggle="collapse"
                                :data-bs-target="`#collapseTeacher-${student.id}-${teacher.id}`" aria-expanded="true"
                                :aria-controls="`collapseTeacher-${student.id}-${teacher.id}`">
                                <b>{{ teacher.subject.name }}</b>
                                <span v-if="teacher.extra_subjects.length">,&nbsp;<span v-for="sb, index in teacher.extra_subjects" :key="sb.id">{{ sb.name }}<span v-if="index + 1 != teacher.extra_subjects.length">, </span></span></span>
                                &nbsp;({{ teacher.author.short_name }})
                              </button>
                            </h2>
                            <div :id="`collapseTeacher-${student.id}-${teacher.id}`"
                              class="accordion-collapse collapse"
                              :data-bs-parent="`#accordionTeacher-${student.id}-${teacher.id}`">
                              <div class="accordion-body">
                                <div class="my-1 d-flex align-items-center" v-if="teacher.extra_subjects.length">
                                  <div class="me-2">Дополнительные предметы:</div>
                                  <div><span v-for="sb, index in teacher.extra_subjects" :key="sb.id">{{ sb.name }}<span v-if="index + 1 != teacher.extra_subjects.length">, </span></span></div>
                                </div>
                                <div class="my-2"
                                  v-if="teacher.criterion_achievements && teacher.criterion_achievements.length">
                                  <div class="my-2"><b>Результаты по критериям</b></div>
                                  <table class="table table-sm table-bordered">
                                    <thead>
                                      <tr>
                                        <td>Критерий</td>
                                        <td>Результат</td>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr v-for="cr in teacher.criterion_achievements" :key="cr.id">
                                        <td>{{ cr.criterion_name }}</td>
                                        <td><b>{{ cr.achievement_name || 'Нет оценки' }}</b></td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>
                                <div class="my-2" v-if="teacher.topic_achievements && teacher.topic_achievements.length">
                                  <div class="my-2"><b>Результаты по темам</b></div>
                                  <table class="table table-sm table-bordered">
                                    <thead>
                                      <tr>
                                        <th scope="col" style="width: 50%;">Тема</th>
                                        <th scope="col" style="min-width: 60px;">Кр.</th>
                                        <th scope="col" style="width: 50%;">Комментарий</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr v-for="achieve in teacher.topic_achievements" :key="achieve.id">
                                        <td>{{ achieve.topic.name }}</td>
                                        <td><span v-if="achieve.level">{{ achieve.level.toUpperCase() || '-' }}</span>
                                        </td>
                                        <td>{{ achieve.comment || 'Нет комментариев' }}</td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>
                                <div class="my-2" v-if="teacher.objective_levels && teacher.objective_levels.length">
                                  <div class="my-2"><b>Уровни достижений по MYP</b></div>
                                  <div v-for="objective in teacher.objective_levels" :key="objective.id">
                                    <div>
                                      {{ objective.objective_letter.toUpperCase() }}{{ objective.strand_letter }}.
                                      Students
                                      should be able to {{ objective.strand_name }}:
                                    </div>
                                    <div class="ms-3">
                                      <em>
                                      The student {{ objective.level_name ||
                                        'does not reach a standard described by any of thedescriptors below' }}
                                        </em>
                                    </div>
                                  </div>
                                </div>
                                <div class="my-2" v-if="teacher.criterion_marks && teacher.criterion_marks.length">
                                  <div class="my-2"><b>Оценки по критериям MYP</b></div>
                                  <table class="table table-sm table-bordered">
                                    <thead>
                                      <tr>
                                        <td>Критерий</td>
                                        <td>Балл</td>
                                        <td>Сумма</td>
                                        <td>Оценка</td>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr v-for="cr, index in teacher.criterion_marks" :key="cr.id">
                                        <td>{{ cr.criterion_letter.toUpperCase() }}. {{ cr.criterion_name }}</td>
                                        <td><b>{{ cr.mark }}</b></td>
                                        <template v-if="index == 0">
                                          <td :rowspan="teacher.criterion_marks.length">
                                            {{ calculateSumMark(teacher.criterion_marks).summ }} / {{ teacher.criterion_marks.length * 8 }}
                                          </td>
                                          <td :rowspan="teacher.criterion_marks.length">
                                            {{ calculateSumMark(teacher.criterion_marks).mark }}
                                          </td>
                                        </template>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>
                                <div class="my-2" v-if="teacher.final_grade_ib">
                                  Итоговая оценка IB: <b>{{ teacher.final_grade_ib }}</b>
                                </div>
                                <div class="my-2" v-if="teacher.final_grade">Итоговая оценка: <b>{{
                                  teacher.final_grade }}</b>
                                </div>
                                <hr />
                                <div class="my-2 text-muted" v-html="teacher.comment" v-if="teacher.comment"></div>
                                <div v-else>Нет информации</div>
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
    </transition>
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
import { resolveBlob } from "@/common/helpers/download";
import { calculateSumMark } from "@/common/helpers/criteria";
import { formatDate } from "@/common/helpers/date";

import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";

import GroupClasses from "@/modules/GroupClasses.vue";
import ReportMentorIbProfile from "@/modules/ReportMentorIbProfile.vue";
import ReportMentorPrimaryUnit from "@/modules/ReportMentorPrimaryUnit.vue";
import EventParticipation from "@/modules/EventParticipation.vue";

import { useGeneralStore } from "@/stores/general";
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";
import { useIboStore } from "@/stores/ibo";


const currentAcademicYear = ref({});
const currentReportPeriod = ref({});
const currentGroup = ref({});
const currentStudent = ref({});

const generalStore = useGeneralStore();
const reportStore = useReportStore();
const authStore = useAuthStore();
const iboStore = useIboStore();

const isEditing = ref(false);
let confirmationModal = null;
const isLoadedReport = ref(false)

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

const isLoadedFilters = computed(() => {
  return reportStore.reportPeriods.length && generalStore.groups.length && generalStore.academicYears.length
})

// Вспомогательная функция для проверки разрешения редактирования репорта только автору или воспитателю этого класса
const isAuthor = (report) => {
  if (authStore.user) {
    return !report || report && report.author.id == authStore.user.id || authStore.user.group_roles.some(item => item.group.id == currentGroup.value.id && item.role == 'Воспитатель')
  }
  return false
}

// Вспомогательная функция для проверки разрешения создания репорта только ментору
const isMentor = () => {
  if (authStore.user) {
    return authStore.user.mentor_classes.some(item => item.id == currentGroup.value.id)
  }
  return false
}

function isPropertyFilledInEveryObject(array, propertyName) {
  return array.every(obj => obj[propertyName] !== undefined && obj[propertyName] !== null && obj[propertyName] !== '');
}

const checkReportComplete = (report) => {
  if (isEmpty(currentGroup.value)) {
    return false
  }
  if (currentGroup.value.curriculum.level == "noo") {
    return report.comment && report.profiles.length && isPropertyFilledInEveryObject(report.profiles, 'level') && report.pyp_units.length && isPropertyFilledInEveryObject(report.pyp_units, 'comment')
  } else {
    return report.comment 
  } 
}

const currentReportType = computed(() => {
  if (isEmpty(currentGroup.value)) {
    return
  }
  if (currentGroup.value.curriculum.level == 'noo') {
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
    (item) => item.year_study.id == currentGroup.value.curriculum.id
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
  resetSelectedReportPeriod();
  resetSelectedGroup();
  resetStudents();
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
const getStudentMentorReports = async () => {
  // console.log('Запрос студентов с репортами')
  if (
    isEmpty(currentAcademicYear.value) ||
    isEmpty(currentGroup.value)
  ) {
    return null;
  }
  isLoadedReport.value = true;
  await reportStore
    .loadStudentMentorReports({
      params: {
        groups: 3,
        classes: currentGroup.value.id,
        report_period: currentReportPeriod.value.id,
        report_group: currentGroup.value.id,
      },
    });
  isLoadedReport.value = false;
};

// Запрос на создание репорта для студента:
// Нужно выбрать период и класс
// После успешного ответа происходит повторный запрос на обновление списка студентов
const createStudentMentorReport = (id) => {
  // console.log('Запрос на создание репорта для студента')
  if (isEmpty(currentReportPeriod.value) || isEmpty(currentGroup.value)) {
    return null;
  }
  if (currentGroup.value.curriculum.level == "noo") {
    reportStore
      .createReportMentorPrimary({
        student: id,
        author: authStore.user.id,
        period: currentReportPeriod.value.id,
        group: currentGroup.value.id,
      })
      .then((result) => {
        authStore.showMessageSuccess('Репорт наставника начальной школы создан');
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
        authStore.showMessageSuccess('Репорт наставника создан');
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
  if (isEmpty(currentGroup.value)) {
    return
  }
  if (currentGroup.value.curriculum.level == "noo") {
    reportStore
      .removeReportMentorPrimary(currentStudent.value.report.id)
      .then((result) => {
        authStore.showMessageSuccess('Репорт наставника начальной школы удалён');
        getStudentMentorReports();
      });
  } else {
    reportStore
      .removeReportMentor(currentStudent.value.report.id)
      .then((result) => {
        authStore.showMessageSuccess('Репорт наставника удалён');
        getStudentMentorReports();
      });
  }
  confirmationModal.hide();
};

// Запрос на сохранение данных из компонента редактирования
// После успешного ответа происходит повторный запрос на обновление списка студентов
const handleSave = async (editData, id) => {
  // console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  if (isEmpty(currentGroup.value)) {
    return
  }
  const updatedObject = {
    id: id,
    [editData.propName]: editData.value,
  };
  if (currentGroup.value.curriculum.level == "noo") {
    reportStore.updateReportMentorPrimary(updatedObject).then((result) => {
      authStore.showMessageSuccess('Сохранено');
      getStudentMentorReports();
    });
  } else {
    reportStore.updateReportMentor(updatedObject).then((result) => {
      authStore.showMessageSuccess('Сохранено');
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

onMounted(async () => {
  recoveryOptions();
  if (!generalStore.isAcademicYearsLoaded) {
    await generalStore.loadAcademicYears();
  } 
  currentAcademicYear.value = generalStore.relevantYear;
  getGroups();
  getStudentMentorReports();
  reportStore.loadReportPeriods();
  iboStore.loadLearnerProfiles();
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});

const exportReportToWord = (student) => {
  if (isEmpty(currentGroup.value)) {
    return
  }
  let config = {
    responseType: 'blob',
    params: {
      report_period: currentReportPeriod.value.id,
      report_group: currentGroup.value.id,
    }
  }
  if (currentGroup.value.curriculum.level == 'noo') {
    config.params.level = 'noo';
  } else if (currentGroup.value.curriculum.level == 'ooo') {
    config.params.level = 'ooo';
  } else if (currentGroup.value.curriculum.level == 'soo') {
    config.params.level = 'soo';
  }
  reportStore.exportStudentMentorReport(student.id, config).then((result) => {
    console.log(result);
    resolveBlob(result);
  });

}

</script>

<style scoped>
.no-report {
  color: grey!important;
}
.report-complete {
  background-color: #b0e4af;
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
  transition: opacity 0.5s ease;
}

.card-enter-from,
.card-leave-to {
  opacity: 0;
}
</style>