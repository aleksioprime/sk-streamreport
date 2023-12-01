<template>
  <div>
    <h1>Репорты наставника</h1>
    <div class="py-2">
      <div class="d-flex flex-wrap">
        <div class="m-2">
          <simple-dropdown
            title="Выберите учебный год"
            v-model="currentAcademicYear"
            :propItems="generalStore.academicYears"
            showName="name"
            @select="selectAcademicYear"
          />
        </div>
        <div class="m-2">
          <simple-dropdown
            title="Выберите период"
            v-model="currentReportPeriod"
            :propItems="filteredReportPeriod"
            showName="full_name"
            :disabled="!Boolean(filteredReportPeriod.length)"
            @select="selectReportPeriod"
          />
        </div>
        <div class="m-2">
          <simple-dropdown
            title="Выберите параллель"
            v-model="currentStudyYear"
            :propItems="generalStore.studyYears"
            showName="name"
            @select="selectStudyYear"
          />
        </div>
        <div class="m-2">
          <simple-dropdown
            title="Выберите класс"
            v-model="currentGroup"
            :propItems="filteredGroup"
            showName="full_name"
            :disabled="
              isEmpty(currentAcademicYear) || isEmpty(currentStudyYear)
            "
            @select="selectGroup"
          />
        </div>
        <button
          type="button"
          class="btn btn-secondary m-2"
          @click="resetSelectedOptions"
        >
          Сброс
        </button>
      </div>
      <button
        type="button"
        class="btn btn-primary m-2"
        @click="getStudentMentorReports"
        :disabled="isEmpty(currentGroup) || isEmpty(currentReportPeriod)"
      >
        Показать студентов
      </button>
      <hr class="hr" />
      <h5 v-if="!isEmpty(currentStudyYear)" class="mb-2">
        Тип репорта: {{ currentStudyYear.level_name }}
      </h5>
      <h5>
        <span v-if="!isEmpty(currentGroup)"
          >Класс: {{ currentGroup.name }}</span
        >
      </h5>
      <div v-if="reportStore.studentMentorReports.length">
        <div
          v-for="student in reportStore.studentMentorReports"
          :key="student.id"
          class="my-3"
        >
          <div class="card my-1">
            <div class="card-body d-flex align-items-center">
              <img
                :src="student.photo ? student.photo : imageStudent"
                alt=""
                width="50"
                class="me-2 rounded-circle"
              />
              <h4 class="m-0">
                {{ student.last_name }} {{ student.first_name }}
              </h4>
              <div class="ms-auto">
                <i
                  class="bi bi-three-dots dot-menu"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                ></i>
                <ul class="dropdown-menu">
                  <li v-if="!student.reports.length">
                    <a
                      class="dropdown-item"
                      href="##"
                      @click="createStudentMentorReport(student.id)"
                      >Добавит репорт</a
                    >
                  </li>
                  <li v-else>
                    <a
                      class="dropdown-item"
                      href="##"
                      @click="showConfirmationModal(student)"
                      >Удалить репорт</a
                    >
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div
            class="accordion"
            :id="`accordionStudent-${student.id}`"
            v-if="student.reports.length"
          >
            <div class="accordion-item">
              <h2 class="accordion-header" :id="`heading-${student.id}`">
                <button
                  class="accordion-button collapsed p-2"
                  :class="{ 'report-success': student.report.comment }"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="`#collapse-${student.id}`"
                  aria-expanded="true"
                  :aria-controls="`collapse-${student.id}`"
                >
                  Репорт студента
                </button>
              </h2>
              <div
                :id="`collapse-${student.id}`"
                class="accordion-collapse collapse"
                :aria-labelledby="`heading-${student.id}`"
              >
                <div class="accordion-body">
                  <div class="my-2">
                    <editable-area-tiny
                      class="text-muted"
                      :propData="student.report.comment"
                      propName="comment"
                      @save="handleSave($event, student.report.id)"
                      :isEditing="isEditing"
                      @toggleEdit="toggleEdit"
                    />
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
        </div>
      </div>
      <div class="card" v-else>
        <div class="card-body">
          <div class="d-flex justify-content-center">
            Выберите необходимые параметры для отображения карточек студентов
          </div>
        </div>
      </div>
    </div>
    <!-- Подключение модального окна -->
    <confirmation-modal
      @confirm="removeStudentMentorReport"
      @cancel="cancelRemoveStudentMentorReport"
    >
      Вы действитель хотите удалить репорт студента:
      <strong
        >{{ currentStudent.last_name }} {{ currentStudent.first_name }}?</strong
      >
    </confirmation-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";
import imageStudent from "@/assets/img/student.svg";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";
import { useGeneralStore } from "@/stores/general";
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";
import { formatDate } from "@/common/helpers/date";

const currentAcademicYear = ref({});
const currentStudyYear = ref({});
const currentReportPeriod = ref({});
const currentGroup = ref({});
const currentStudent = ref({});

const generalStore = useGeneralStore();
const reportStore = useReportStore();
const authStore = useAuthStore();

const isEditing = ref(false);
let confirmationModal = null;

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
    !(isEmpty(currentStudyYear.value) && isEmpty(currentAcademicYear.value))
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
  if (currentStudyYear.value.level == "noo") {
    reportStore
      .loadStudentMentorPrimaryReports({
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
  } else {
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
  }
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
    });
  } else {
    currentAcademicYear.value = generalStore.relevantYear;
  }
  if (!generalStore.isStudyYearsLoaded) {
    generalStore.loadStudyYears();
  }
  if (!reportStore.isReportPeriodsLoaded) {
    reportStore.loadReportPeriods();
  }
  if (!generalStore.isGroupsLoaded) {
    getGroups();
  }
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});
</script>