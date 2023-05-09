<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты учителя</template>
    </base-header>
    <report-filter @updateFetch="updateFetch"/>
    <div v-if="studentsReport.length" class="report-wrapper">
      <report-teacher-item v-for="student in studentsReport" :key="student.id" :period="currentPeriod"
      :student="student" @updateReport="fetchUpdateReport" :criteria="criteriaMYP"/>
    </div>
    <div v-else class="report-none">
      Пока нет данных
    </div>
    
  </div>
</template>

<script>
import ReportFilter from "@/components/assessment/ReportFilter.vue";
import ReportTeacherItem from "@/components/assessment/ReportTeacherItem.vue";
import { getStudentsReport, createReportTeacher, updateReportTeacher } from "@/hooks/assess/useReportTeacher";
import { getCriteriaDetailMYP } from "@/hooks/unit/useCriterionMYP";

export default {
  components: {
    ReportFilter, ReportTeacherItem
  },
  setup(props) {
    const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { createdReportTeacher, fetchCreateReportTeacher } = createReportTeacher();
    const { updatedReportTeacher, fetchUpdateReportTeacher } = updateReportTeacher();
    const { criteriaMYP, fetchGetCriteriaDetailMYP } = getCriteriaDetailMYP();
    return {
      studentsReport, isStudentsReportLoading, fetchGetStudentsReport,
      createdReportTeacher, fetchCreateReportTeacher,
      updatedReportTeacher, fetchUpdateReportTeacher,
      criteriaMYP, fetchGetCriteriaDetailMYP,
    }
  },
  data() {
    return {
      currentReport: {},
      currentFetchData: {},
      currentPeriod: {}
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

  },
  computed: {
  }
}
</script>

<style>
@import '@/assets/css/spinner.css';
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