<template>
  <div class="report-item">
    <div class="student-header">
      <div class="student-photo">
        <img :src='student.user.photo ? student.photo : require("@/assets/img/user.png")' alt="" width="50">
      </div>
      <div class="student-info">
        <div class="student-name">{{ student.user.last_name }} {{ student.user.first_name }}</div>
      </div>
    </div>
    <div class="assess-title">Результаты студента за {{ period.assessment_period.number }} {{ period.assessment_period.type }}</div>
    <div class="student-assessment">
      <div class="assess-wrapper">
        <div class="assess-item">
          <div class="assess-criterion">{{ criterionA.letter }}. {{ criterionA.name_eng }}</div>
          <div class="assess-mark">{{ student.periodassess.criterion_a || '-' }}</div>
        </div>
        <div class="assess-item">
          <div class="assess-criterion">{{ criterionB.letter }}. {{ criterionB.name_eng }}</div>
          <div class="assess-mark">{{ student.periodassess.criterion_b || '-' }}</div>
        </div>
        <div class="assess-item">
          <div class="assess-criterion">{{ criterionC.letter }}. {{ criterionC.name_eng }}</div>
          <div class="assess-mark">{{ student.periodassess.criterion_c || '-' }}</div>
        </div>
        <div class="assess-item">
          <div class="assess-criterion">{{ criterionD.letter }}. {{ criterionD.name_eng }}</div>
          <div class="assess-mark">{{ student.periodassess.criterion_d || '-' }}</div>
        </div>
        <div class="assess-item">
          <div class="assess-form">Текущая оценка</div>
          <div class="assess-mark">{{ student.periodassess.form_grade || '-' }}</div>
        </div>
        <div class="assess-item">
          <div class="assess-final">Итоговая оценка</div>
          <div class="assess-mark">{{ student.periodassess.final_grade || '-' }}</div>
        </div>
      </div>
      <div class="achievements-wrapper">

      </div>
    </div>
    <div class="student-report">
      <report-field-text id="student-report" :student="student" @save="fetchSaveReport"/>
    </div>
    <div class="student-events" v-if="student.teacher_report.id">
      <div>Участие в мероприятиях</div>
      <report-field-blocks id="student-events" :fieldData="student.teacher_report.events" :fieldName="'events'" @save="fetchSaveEvent">
        <!-- Слот для блоков показа записей -->
        <template v-slot:show="field">
          <div class="blocks-wrapper">
            <div>{{ field.data.title }}</div>
            <div>Тип: {{ field.data.type_name }}. Уровень: {{ field.data.level_name }}</div>
            <div>Результаты: {{ field.data.result }}</div>
          </div>
        </template>
        <template v-slot:form="item">  
          <div class="my-2">
            <input class="form-control" type="text" v-model="item.data.title">
            <textarea class="form-control" type="text" v-model="item.data.result"
              placeholder="Описание результатов"></textarea>
          </div>
        </template>
      </report-field-blocks>
    </div>
  </div>
</template>
  
<script>
import ReportFieldText from "@/components/assessment/ReportFieldText.vue";
import ReportFieldBlocks from "@/components/assessment/ReportFieldBlocks.vue";

export default {
  name: 'ReportTeacherItem',
  components: {
    ReportFieldText, ReportFieldBlocks
  },
  props: {
    student: {
      type: Object,
      default: {
        group: {},
        teacher_report: {},
        user: {},
      }
    },
    criteria: {
      type: Array,
      default: []
    },
    period: { Object },
  },

  data() {
    return {
      
    }
  },
  methods: {
    fetchSaveReport(data) {
      console.log('Сохранение репорта: ', data);
      const editReportStudents = {
        student_id: this.student.id,
        text: data.text,
        id: this.student.teacher_report.id || null,
      }
      this.$emit('updateReport', editReportStudents);
    },
    fetchSaveEvent(data) {
      console.log('Сохранение мероприятия: ', data);
      const editReportStudents = {
        student_id: this.student.id,
        events: data.events,
        id: this.student.teacher_report.id || null,
      }
      this.$emit('updateReport', editReportStudents);
    }
  },
  computed: {
    criterionA() {
      return this.criteria.find(item => item.letter == 'A')
    },
    criterionB() {
      return this.criteria.find(item => item.letter == 'B')
    },
    criterionC() {
      return this.criteria.find(item => item.letter == 'C')
    },
    criterionD() {
      return this.criteria.find(item => item.letter == 'D')
    },
  }
}
</script>
  
<style>
.report-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
}

.report-item:hover {
  transition: 1s;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.4);
}

.student-header {
  display: flex;
}

.student-photo {
  margin-right: 10px;
}
.student-name {
  text-transform: uppercase;
  font-size: 1.5em;
  font-weight: 700;
}
.student-info {
  display: flex;
  align-items: center;
}
.assess-title {
  margin-top: 10px;
}
.student-assessment {
  margin-top: 10px;
  display: flex;
  column-gap: 5px;
}

.achievements-wrapper {
  flex-grow: 1;
  border: 0.5px solid #a7a7a78a;
  min-height: 100px;
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .student-assessment {
    flex-direction: column;
  }
}

.assess-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 350px;
  margin-bottom: 10px;
}

.assess-item {
  display: flex;
  align-items: center;
  border-bottom: 0.5px solid #a7a7a78a;
  padding: 0 5px;
}

.assess-criterion:hover {
  font-weight: 700;
  cursor: pointer;
}

.assess-mark {
  font-weight: 700;
  margin-left: auto;
}

.student-report {
  margin-top: 10px;
}</style>