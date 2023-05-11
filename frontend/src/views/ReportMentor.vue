<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты наставника</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear" @change="resetQuery">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
            {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <!-- Выбор периодов обучения -->
    <div class="block-period">
      <div v-for="pr in reportPeriods" :key="pr.id" class="period">
        <input type="radio" name="period" :value="pr" :id="'period-' + pr.id"
          v-model="currentReportPeriod" @change="choicePeriod">
        <label :for="'period-' + pr.id">
        <div class="period-title">{{ pr.number }} период</div>
        <div class="period-item-date">{{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }}</div>
        </label>
      </div>
    </div>
    <div v-if="studentsReport.length" class="report-wrapper">
      <div class="student-list">
        <div v-for="student in studentsReport" :key="student.id">
          <div class="form-check">
            <input class="form-check-input" type="radio" name="student" :value="student" :id="'student-' + student.id"
              v-model="currentStudent">
            <label class="form-check-label" :for="'student-' + student.id">
              <div>{{ student.user.last_name }} {{ student.user.first_name }}</div>
            </label>
          </div>
        </div>
      </div>
      <report-mentor-item :period="currentReportPeriod" v-if="currentStudent" class="student-item"
      :student="currentStudent" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport"/>
      <div v-else>Выберите студента</div>
    </div>
    <div v-else class="report-none">
      Пока нет данных
    </div>
  </div>
</template>

<script>
import ReportMentorItem from "@/components/assessment/ReportMentorItem.vue";
import { getStudentsReport, createReportMentor, updateReportMentor, getReportMentorJournal } from "@/hooks/assess/useReportMentor";
import { getCriteriaDetailMYP } from "@/hooks/unit/useCriterionMYP";
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";

export default {
  components: {
    ReportMentorItem
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();
    const { currentGroup, currentClassYear, eventTypes, fetchGetReportMentorJournal } = getReportMentorJournal();
    const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { createdReportMentor, fetchCreateReportMentor } = createReportMentor();
    const { updatedReportMentor, fetchUpdateReportMentor } = updateReportMentor();
    const { criteriaMYP, fetchGetCriteriaDetailMYP } = getCriteriaDetailMYP();

    return {
      currentGroup, currentClassYear, eventTypes, fetchGetReportMentorJournal,
      studentsReport, isStudentsReportLoading, fetchGetStudentsReport,
      createdReportMentor, fetchCreateReportMentor,
      updatedReportMentor, fetchUpdateReportMentor,
      criteriaMYP, fetchGetCriteriaDetailMYP,
      studyYears, currentStudyYear, fetchGetStudyYears,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
    }
  },
  data() {
    return {
      currentStudent: null,
      currentReport: {},
      eventLevels: [
        { value: '0', name: 'Без уровня' },
        { value: '1', name: '1 уровень' },
        { value: '2', name: '2 уровень' },
        { value: '3', name: '3 уровень' },
      ]
    }
  },
  methods: {
    choicePeriod() {
      this.fetchGetStudentsReport({
        group: this.$route.params.id_group,
        class_year: this.currentClassYear.id,
        period: this.currentReportPeriod.id,
        study_year: this.currentStudyYear.id,
      }).finally(() => {
        this.currentStudent = this.studentsReport.find(item => this.currentStudent.id == item.id);
      });
    },
    fetchUpdateReport(editingReport) {
      editingReport.period_id = this.currentReportPeriod.id;
      editingReport.year_id = this.currentClassYear.id;
      console.log('Запрос на добавление или обновление данных: ', editingReport)
      if (editingReport.id) {
        this.setStudentReportUpdate(editingReport);
      } else {
        this.setStudentReportCreate(editingReport);
      }
    },
    setStudentReportCreate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на добавление данных: ", fetchData);
        this.fetchCreateReportMentor(fetchData).finally(() => {
          // this.replaceTextReport(fetchData.student_id, fetchData.text);
          this.fetchGetStudentsReport({
            group: this.$route.params.id_group,
            class_year: this.currentClassYear.id,
            period: this.currentReportPeriod.id,
            study_year: this.currentStudyYear.id,
          });
        });
      }
    },
    setStudentReportUpdate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на изменение данных: ", fetchData);
        this.fetchUpdateReportMentor(fetchData).finally(() => {
          // this.replaceTextReport(fetchData.student_id, fetchData.text);
          this.fetchGetStudentsReport({
            group: this.$route.params.id_group,
            class_year: this.currentClassYear.id,
            period: this.currentReportPeriod.id,
            study_year: this.currentStudyYear.id,
          });
        });
      }
    },
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear }).finally(() => {
        this.fetchGetReportMentorJournal({
          group: this.$route.params.id_group, 
          period: this.currentReportPeriod.id,
        }).finally(() => {
          this.fetchGetStudentsReport({
            group: this.$route.params.id_group,
            class_year: this.currentClassYear.id,
            period: this.currentReportPeriod.id,
            study_year: this.currentStudyYear.id,
          }).finally(() => {
            this.currentStudent = this.studentsReport[0];
          });
        })
      })
    });

    
  },
}
</script>

<style>
@import '@/assets/css/spinner.css';

.student-list {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  margin-bottom: 20px;
}
.student-item {
  
}
</style>