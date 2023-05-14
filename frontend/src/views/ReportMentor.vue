<template>
  <div>
    <base-header>
      <template v-slot:header>Репорты наставника</template>
    </base-header>
    <div class="col-md mb-2">
      <div>Период репорта: <b>{{ currentReportPeriod.name }}</b></div>
      <div>Класс: <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> 
      <br>Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }}</div>
    </div>
    <div v-if="!isStudentsReportLoading && !firstLoading">
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
        <report-mentor-item :period="currentReportPeriod" v-if="currentStudent" class="student-item" :criteria="criteriaMYP"
        :student="currentStudent" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport"/>
        <div v-else>Выберите студента</div>
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
import ReportMentorItem from "@/components/assessment/ReportMentorItem.vue";
import { getStudentsReport, createReportMentor, updateReportMentor, getReportMentorJournal } from "@/hooks/assess/useReportMentor";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";

export default {
  components: {
    ReportMentorItem
  },
  setup(props) {
    const { currentGroup, currentReportPeriod, eventTypes, fetchGetReportMentorJournal } = getReportMentorJournal();
    const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { createdReportMentor, fetchCreateReportMentor } = createReportMentor();
    const { updatedReportMentor, fetchUpdateReportMentor } = updateReportMentor();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();

    return {
      currentGroup, currentReportPeriod, eventTypes, fetchGetReportMentorJournal,
      studentsReport, isStudentsReportLoading, fetchGetStudentsReport,
      createdReportMentor, fetchCreateReportMentor,
      updatedReportMentor, fetchUpdateReportMentor,
      criteriaMYP, fetchGetCriteriaMYP,
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
      ],
      currentFetchData: {},
      firstLoading: true,
    }
  },
  methods: {
    fetchUpdateReport(editingReport) {
      editingReport.period_id = this.currentReportPeriod.id;
      editingReport.year_id = this.currentGroup.class_year.id;
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
          this.fetchGetStudentsReport(this.currentFetchData).finally(() => {
            this.currentStudent = this.studentsReport.find(item => item.id == this.createdReportMentor.student.id);
          });
        });
      }
    },
    setStudentReportUpdate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на изменение данных: ", fetchData);
        this.fetchUpdateReportMentor(fetchData).finally(() => {
          this.fetchGetStudentsReport(this.currentFetchData).finally(() => {
            this.currentStudent = this.studentsReport.find(item => item.id == this.updatedReportMentor.student.id);
          });
        });
      }
    },
  },
  mounted() {
    this.fetchGetReportMentorJournal({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
    }).finally(() => {
      this.currentFetchData = {
        group: this.currentGroup.id,
        class_year: this.currentGroup.class_year.id,
        period: this.currentReportPeriod.id,
      }
      this.fetchGetStudentsReport(this.currentFetchData).finally(() => {
        this.currentStudent = this.studentsReport[0];
        this.firstLoading = false;
        this.fetchGetCriteriaMYP({});
      });
    })
  },
}
</script>

<style>
@import '@/assets/css/spinner.css';
.loader {
  display: flex;
  height: calc(100vh - 200px);
  align-items: center;
  justify-content: center;
}
.student-list {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  margin-bottom: 20px;
}
.student-item {
  
}
</style>