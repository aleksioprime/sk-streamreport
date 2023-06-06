<template>
  <div>
    <base-header>
      <template v-slot:link><a href="#" @click="$router.push(`/report/mentor`)" >Вернуться к выбору класса</a></template>
      <template v-slot:header>Репорты наставника</template>
    </base-header>
    <transition name="fade">
      <div>
        <div class="col-md mb-2" v-if="currentReportPeriod.name">
          <div>Период репорта: <b>{{ currentReportPeriod.name }}</b></div>
          <div>Класс: <b>{{ currentGroup.group_name }}</b>  ({{ getWordStudent(currentGroup.count) }}) 
          <br><span v-if="currentGroup.mentor">Наставник: {{ currentGroup.mentor.full_name }}</span> 
          <br><span v-if="currentGroup.psychologist">Психолог: {{ currentGroup.psychologist.full_name }}</span></div>
        </div>
        <div v-if="!isStudentReportLoading || !firstLoading">
          <div v-if="currentStudentId" class="report-wrapper">
            <div class="student-list radiobutton">
              <div v-for="student in currentGroup.students" :key="student.id">
                <input type="radio" name="student" :value="student.id" :id="'student-' + student.id"
                  v-model="currentStudentId" @change="choiceStudent">
                <label :for="'student-' + student.id" :class="getStyleForStudent(student)">
                  <div>{{ student.short_name }}</div>
                </label>
              </div>
            </div>
            <report-mentor-item :period="currentReportPeriod" v-if="studentReport.id" class="student-item" :program="currentGroup.program" :subjects="subjects"
            :student="studentReport" :types="eventTypes" :levels="eventLevels" @updateReport="fetchUpdateReport" :editable="currentGroup.mentor.id == authUser.teacher.id"/>
            <!-- <div v-else>Выберите студента</div> -->
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
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ReportMentorItem from "@/components/assessment/ReportMentorItem.vue";
import { getStudentReport, createReportMentor, updateReportMentor, getReportMentorJournal } from "@/hooks/assess/useReportMentor";

export default {
  components: {
    ReportMentorItem
  },
  setup(props) {
    const { currentGroup, subjects, currentReportPeriod, eventTypes, fetchGetReportMentorJournal } = getReportMentorJournal();
    const { studentReport, isStudentReportLoading,  fetchGetStudentReport } = getStudentReport();
    const { createdReportMentor, fetchCreateReportMentor } = createReportMentor();
    const { updatedReportMentor, fetchUpdateReportMentor } = updateReportMentor();

    return {
      currentGroup, subjects, currentReportPeriod, eventTypes, fetchGetReportMentorJournal,
      studentReport, isStudentReportLoading, fetchGetStudentReport,
      createdReportMentor, fetchCreateReportMentor,
      updatedReportMentor, fetchUpdateReportMentor,
    }
  },
  data() {
    return {
      currentStudentId: null,
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
    getStyleForStudent(student) {
      const studentInReport = this.currentGroup.reports.find(item => item.student_id == student.id && item.period == this.currentReportPeriod.id)
      if (studentInReport) {
        if (studentInReport.check_text) {
          return 'check-text'
        }
        // return 'check-student'
      }
    },
    choiceStudent() {
      this.fetchGetStudentReport(this.currentStudentId, this.currentFetchData)
    },
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    // В сигнале на сохранение данные из компонента проверяется, есть ли ID репорта
    // и если его нет, то вызывается функция создания репорта, а если есть, то обновления
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
    // Создание нового репорта
    setStudentReportCreate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на добавление данных: ", fetchData);
        this.fetchCreateReportMentor(fetchData).finally(() => {
          this.fetchGetStudentReport(this.currentStudentId, this.currentFetchData);
        });
      }
    },
    // Обновление выбранного репорта
    setStudentReportUpdate(fetchData) {
      if (Object.keys(fetchData).length) {
        console.log("Запрос на изменение данных: ", fetchData);
        this.fetchUpdateReportMentor(fetchData).finally(() => {
          this.fetchGetStudentReport(this.currentStudentId, this.currentFetchData);
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
      this.currentStudentId = this.currentGroup.students[0].id
      this.fetchGetStudentReport(this.currentStudentId, this.currentFetchData);
    })
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin', 'isDnevnik']),
  }
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.student-list {
  display: flex;
  flex-wrap: wrap;
  column-gap: 5px;
  row-gap: 5px;
  margin-bottom: 20px;
}
.check-text {
  /* color: #fff; */
  color: var(--bs-secondary);
  font-weight: 700;
  /* border: 1px solid var(--bs-secondary);
  border-radius: 5px; */
}
.check-student {
  color: var(--bs-secondary);
  /* border: 1px solid var(--bs-secondary);
  border-radius: 5px; */
}

</style>