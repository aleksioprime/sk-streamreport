<template>
  <div>
    <base-header>
      <template v-slot:link><a href="#" @click="$router.push(`/assessment/group`)" >Вернуться к выбору класса</a></template>
      <template v-slot:header>Репорты учителя</template>
    </base-header>
    <!-- <report-filter @updateFetch="updateFetch"/> -->
    <div class="col-md mb-2">
      <div>Период репорта: <b>{{ currentReportPeriod.name }}</b></div>
      <div>Класс: <b>{{ currentGroup.class_year.year_rus }}{{ currentGroup.letter }}</b> ({{ getWordStudent(currentGroup.count) }}) 
      <br>Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }}
      <br><span v-if="currentGroup.psychologist">Психолог: {{ currentGroup.psychologist.user.last_name }} {{ currentGroup.psychologist.user.first_name }} {{ currentGroup.psychologist.user.middle_name }}</span> 
    </div>
      <div>Предмет: <b>{{ currentSubject.name_rus }} ({{ currentSubject.group_ib.name_eng }})</b></div>
    </div>
    <button class="btn btn-primary mt-2" @click="showClassModal">Изменить список группы</button>
    <div v-if="!isReportsTeacherLoading || !firstLoading">
      <div v-if="reportsTeacher.length" class="report-wrapper">
        <report-teacher-item v-for="report in reportsTeacher" :key="report.id" :period="currentReportPeriod" :program="currentSubject.group_ib.program"
        :report="report" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport" :criteria="criteriaMYP" :group="currentGroup"/>
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
    <modal-class @save="saveClassModal" @cancel="hideClassModal" :modalTitle="modalTitleClass">
      <report-teacher-form v-if="!isReportsTeacherLoading" v-model:reportStudents="reportStudents" :group="currentGroup"/>
      <div v-else>Данные загружаются</div>
    </modal-class>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';

import ReportFilter from "@/components/assessment/ReportFilter.vue";
import ReportTeacherItem from "@/components/assessment/ReportTeacherItem.vue";
import { getReportsTeacher, getReportTeacherJournal, createReportTeacher, updateReportTeacher } from "@/hooks/assess/useReportTeacher";
import { getCriteriaMYP } from "@/hooks/unit/useCriterionMYP";
import ReportTeacherForm from "@/components/assessment/ReportTeacherForm.vue";

export default {
  components: {
    ReportFilter, ReportTeacherItem, ReportTeacherForm
  },
  setup(props) {
    // const { studentsReport, isStudentsReportLoading, fetchGetStudentsReport } = getStudentsReport();
    const { currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportTeacher } = getReportTeacherJournal();
    const { reportsTeacher, isReportsTeacherLoading, fetchGetReportsTeacher } = getReportsTeacher();
    const { createdReportTeacher, fetchCreateReportTeacher } = createReportTeacher();
    const { updatedReportTeacher, fetchUpdateReportTeacher } = updateReportTeacher();
    const { criteriaMYP, fetchGetCriteriaMYP } = getCriteriaMYP();
    return {
      // studentsReport, isStudentsReportLoading, fetchGetStudentsReport,
      currentReportPeriod, currentSubject, currentGroup, eventTypes, fetchGetReportTeacher,
      reportsTeacher, isReportsTeacherLoading, fetchGetReportsTeacher,
      createdReportTeacher, fetchCreateReportTeacher,
      updatedReportTeacher, fetchUpdateReportTeacher,
      criteriaMYP, fetchGetCriteriaMYP,
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
      modalTitleClass: null,
      reportStudents: []
    }
  },
  methods: {
    showClassModal() {
      this.modalTitleClass = "Изменение списка для репортов";
      this.reportStudents = [...this.reportsTeacher]
      this.modalClass.show();
    },
    // Изменение состава оценочной группы итоговой работы
    async saveClassModal() {
      const dataStudents = {
        "bulk_create": {
          "students": this.reportStudents.map(item => { return {
            'id': item.id || null,
            'student_id': item.student.id,
          } }),
          'group_id': this.currentGroup.id,
          'year_id': this.currentFetchData.class_year, 
          'period_id': this.currentFetchData.period,
          'subject_id': this.currentFetchData.subject,
        }
        
      }
      console.log('Отправка запроса на добавление студентов в репорты: ', dataStudents);
      await this.axios.post('/assessment/report/teacher', dataStudents).then((response) => {
        console.log('Репорты успешно созданы: ', response.data)
        this.fetchGetReportsTeacher(this.currentFetchData);
      });
      this.hideClassModal();
    },
    hideClassModal() {
      this.modalClass.hide();
    },
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    // updateFetch(data) {
    //   console.log('Обновление данных: ', data)
    //   this.currentFetchData = data;
    //   this.currentPeriod = data.period;
    //   this.currentFetchData.period = data.period.id;
    //   if (Object.values(this.currentFetchData).every(item => item != null)) {
    //     this.fetchGetCriteriaDetailMYP({ subject: this.currentFetchData.subject }).finally(() => {
    //       // this.fetchGetStudentsReport(this.currentFetchData);
    //     });
    //   } else {
    //     this.studentsReport = []
    //   }
    // },
    fetchUpdateReport(editingReport) {
      editingReport.period_id = this.currentFetchData.period;
      editingReport.subject_id = this.currentFetchData.subject;
      editingReport.year_id = this.currentFetchData.class_year;
      console.log("Запрос на изменение данных: ", editingReport);
      this.fetchUpdateReportTeacher(editingReport).finally(() => {
        const index = this.reportsTeacher.findIndex(item => item.id == editingReport.id);
        if (index != -1) {
          this.reportsTeacher[index] = this.updatedReportTeacher
        }
      });
    },
    // Обновление данных до загрузки новых
    // replaceTextReport(id, data) {
    //   this.studentsReport.forEach((item) => {
    //     if (item.id == id) {
    //       item.teacher_report.text = data;
    //     }
    //   })
    //   console.log(this.studentsReport);
    // },
    // setStudentReportCreate(fetchData) {
    //   if (Object.keys(fetchData).length) {
    //     console.log("Запрос на добавление данных: ", fetchData);
    //     this.fetchCreateReportTeacher(fetchData).finally(() => {
    //       this.fetchGetStudentsReport(this.currentFetchData);
    //     });
    //   }
    // },
    // setStudentReportUpdate(fetchData) {
    //   if (Object.keys(fetchData).length) {
    //     console.log("Запрос на изменение данных: ", fetchData);
    //     this.fetchUpdateReportTeacher(fetchData).finally(() => {
    //       const index = this.reportsTeacher.findIndex(item => item.id == fetchData.id);
    //       if (index != -1) {
    //         this.reportsTeacher[index] = this.updatedReportTeacher
    //       }
    //     });
    //   }
    // },
  },
  mounted() {
    this.modalClass = new Modal(`#modalClass`, { backdrop: 'static' });
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
      this.fetchGetCriteriaMYP({ 
        subject: this.currentSubject.id
      }).finally(() => {
        this.fetchGetReportsTeacher(this.currentFetchData).finally(() => {
          this.firstLoading = false;
        });
      });
    });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin', 'isDnevnik']),
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