<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты учителя</template>
    </base-header>
    <!-- <report-filter @updateFetch="updateFetch"/> -->
    <div class="col-md mb-2">
      <div>Период репорта: <b>{{ currentReportPeriod.name }}</b></div>
      <div>Класс: <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> 
      <br>Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }}</div>
      <div>Предмет: <b>{{ currentSubject.name_rus }} ({{ currentSubject.group_ib.name_eng }})</b></div>
    </div>
    <div v-if="!isStudentsReportLoading || !firstLoading">
      <div v-if="studentsReport.length" class="report-wrapper">
        <report-teacher-item v-for="student in studentsReport" :key="student.id" :period="currentReportPeriod" :levelSubject="levels"
        :student="student" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport" :criteria="criteriaMYP"/>
      </div>
      <div v-else class="report-none">
        Пока нет данных
      </div>
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import ReportFilter from "@/components/assessment/ReportFilter.vue";
import ReportTeacherItem from "@/components/assessment/ReportTeacherItem.vue";
import { getStudentsReport, getReportTeacherJournal, createReportTeacher, updateReportTeacher } from "@/hooks/assess/useReportTeacher";
import { getCriteriaDetailMYP } from "@/hooks/unit/useCriterionMYP";
import { getLevels } from "@/hooks/unit/useLevel";

export default {
  components: {
    ReportFilter, ReportTeacherItem
  },
  setup(props) {
    const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportTeacher } = getReportTeacherJournal();
    const { createdReportTeacher, fetchCreateReportTeacher } = createReportTeacher();
    const { updatedReportTeacher, fetchUpdateReportTeacher } = updateReportTeacher();
    const { criteriaMYP, fetchGetCriteriaDetailMYP } = getCriteriaDetailMYP();
    const { levels, fetchGetLevels } = getLevels();
    return {
      studentsReport, isStudentsReportLoading, fetchGetStudentsReport,
      currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportTeacher,
      createdReportTeacher, fetchCreateReportTeacher,
      updatedReportTeacher, fetchUpdateReportTeacher,
      criteriaMYP, fetchGetCriteriaDetailMYP,
      levels, fetchGetLevels
    }
  },
  data() {
    return {
      currentReport: {},
      currentFetchData: {},
      currentPeriod: {},
      eventLevels: [
        { value: '0', name: 'Без уровня' },
        { value: '1', name: '1 уровень' },
        { value: '2', name: '2 уровень' },
        { value: '3', name: '3 уровень' },
      ],
      firstLoading: true,
    }
  },
  methods: {
    updateFetch(data) {
      console.log('Обновление данных: ', data)
      this.currentFetchData = data;
      this.currentPeriod = data.period;
      this.currentFetchData.period = data.period.id;
      if (Object.values(this.currentFetchData).every(item => item != null)) {
        this.fetchGetCriteriaDetailMYP({ subject: this.currentFetchData.subject }).finally(() => {
          this.fetchGetStudentsReport(this.currentFetchData);
        });
      } else {
        this.studentsReport = []
      }
    },
    fetchUpdateReport(editingReport) {
      editingReport.period_id = this.currentFetchData.period;
      editingReport.subject_id = this.currentFetchData.subject;
      editingReport.year_id = this.currentFetchData.class_year;
      console.log('Запрос на добавление или обновление данных: ', editingReport)
      if (editingReport.id) {
        this.setStudentReportUpdate(editingReport);
      } else {
        this.setStudentReportCreate(editingReport);
      }
    },
    // Обновление данных до загрузки новых
    replaceTextReport(id, data) {
      this.studentsReport.forEach((item) => {
        if (item.id == id) {
          item.teacher_report.text = data;
        }
      })
      console.log(this.studentsReport);
    },
    setStudentReportCreate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на добавление данных: ", fetchData);
        this.fetchCreateReportTeacher(fetchData).finally(() => {
          // this.replaceTextReport(fetchData.student_id, fetchData.text);
          this.fetchGetStudentsReport(this.currentFetchData);
        });
      }
    },
    setStudentReportUpdate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на изменение данных: ", fetchData);
        this.fetchUpdateReportTeacher(fetchData).finally(() => {
          // this.replaceTextReport(fetchData.student_id, fetchData.text);
          this.fetchGetStudentsReport(this.currentFetchData);
        });
      }
    },
  },
  mounted() {
    this.fetchGetReportTeacher({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject, 
    }).finally(() => {
      this.currentFetchData = {
        group: this.currentGroup.id,
        class_year: this.currentGroup.class_year.id,
        period: this.currentReportPeriod.id,
        subject: this.currentSubject.id,
      }
      this.fetchGetLevels({ subject: this.currentSubject.id });
      this.fetchGetCriteriaDetailMYP({ 
        subject: this.currentSubject.id
      }).finally(() => {
        this.fetchGetStudentsReport(this.currentFetchData).finally(() => {
          this.firstLoading = false;
        });
      });
    });
  },
  computed: {
  }
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.loader {
  display: flex;
  height: calc(100vh - 200px);
  align-items: center;
  justify-content: center;
}
.report-wrapper {
  margin-top: 20px;
}
.report-none {
  min-height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>