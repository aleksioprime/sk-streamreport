<template>
  <div>
    <h1>Репорты службы сопровождения</h1>
    <div class="py-2">
      <div class="d-flex flex-wrap">
        <div class="m-2">
          <simple-dropdown title="Выберите учебный год" v-model="currentAcademicYear"
            :propItems="generalStore.academicYears" showName="name" @select="selectAcademicYear" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите период" v-model="currentReportPeriod" :propItems="filteredReportPeriod"
            showName="full_name" :disabled="!Boolean(filteredReportPeriod.length)" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите параллель" v-model="currentStudyYear" :propItems="generalStore.studyYears"
            showName="name" @select="selectStudyYear" />
        </div>
        <div class="m-2">
          <simple-dropdown title="Выберите класс" v-model="currentGroup" :propItems="generalStore.groups"
            showName="full_name" :disabled="isEmpty(currentAcademicYear) || isEmpty(currentStudyYear)" />
        </div>
      </div>
      <button type="button" class="btn btn-primary m-2" @click="getStudentExtraReports">Показать студентов</button>
      <hr class="hr">
      <div class="card">
        <div class="card-body">
          <div class="d-flex justify-content-center">Выберите необходимые параметры для отображения карточек студентов
          </div>
          {{ reportStore.studentExtraReports }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import { useGeneralStore } from "@/stores/general";
import { useReportStore } from "@/stores/report";

const currentAcademicYear = ref({})
const currentStudyYear = ref({})
const currentReportPeriod = ref({})
const currentGroup = ref({})

const generalStore = useGeneralStore();
const reportStore = useReportStore();

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
}

// Фильтр списка периодов репорта по выбранному учебному году  
const filteredReportPeriod = computed(() => {
  return reportStore.reportPeriods.filter(item =>
    item.year.id == currentAcademicYear.value.id
  )
});

// Событие выбора учебного года из выпадающего списка 
const selectAcademicYear = () => {
  currentStudyYear.value = {}
  currentReportPeriod.value = {}
  currentGroup.value = {}
}

// Событие выбора учебной параллели из выпадающего списка
const selectStudyYear = () => {
  if (!(isEmpty(currentStudyYear) && isEmpty(currentAcademicYear))) {
    generalStore.loadGroups({
      params: {
        year_study: currentStudyYear.value.id,
        year_academic: currentAcademicYear.value.id
      }
    });
  }
}

const getStudentExtraReports = () => {
  console.log('Запрос студентов с репортами')
  reportStore.loadStudentExtraReports({
    params: {
      groups: 3,
      classes: currentGroup.value.id,
      report_period: currentReportPeriod.value.id,
      report_group: currentGroup.value.id,
    }
  }).then(() => {
    console.log(reportStore.studentExtraReports)
  });
 
}

// Запросы и установки при монтировании компонента
onMounted(() => {
  if (!generalStore.isAcademicYearsLoaded) {
    generalStore.loadAcademicYears().then(() => {
      currentAcademicYear.value = generalStore.relevantYear
    });
  } else {
    currentAcademicYear.value = generalStore.relevantYear
  }
  if (!generalStore.isStudyYearsLoaded) {
    generalStore.loadStudyYears();
  }
  if (!reportStore.isReportPeriodsLoaded) {
    reportStore.loadReportPeriods();
  }
  if (!generalStore.isGroupsLoaded) {
    generalStore.groups = []
  }
});
</script>

<style scoped>
</style>