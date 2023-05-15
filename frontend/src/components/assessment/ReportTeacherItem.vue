<template>
  <div class="report-item area">
    <div class="student-header">
      <div class="student-photo">
        <img :src='student.user.photo ? student.photo : require("@/assets/img/student.svg")' alt="" width="50">
      </div>
      <div class="student-info">
        <div class="student-name">{{ student.user.last_name }} {{ student.user.first_name }}</div>
      </div>
    </div>
    <div class="assess-title selected" data-bs-toggle="collapse" :href="`#collapse-assessment-${student.id}`" role="button" aria-expanded="false" :aria-controls="`collapse-assessment-${student.id}`">
      Результаты студента за <span v-for="(asper, index) in period.assessment_periods" :key="asper.id">{{ asper.number }} {{ asper.type }}<span v-if="++index != period.assessment_periods.length">, </span> </span></div>
    <div :id="`collapse-assessment-${student.id}`" class="collapse">
      <div class="student-assessment" >
        <div class="assess-wrapper">
          <div class="assess-item clicked" @click="getObjectivesFromCriteria(criterionA)">
            <div class="assess-criterion">{{ criterionA.letter }}. {{ criterionA.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.criteria_a, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item clicked" @click="getObjectivesFromCriteria(criterionB)">
            <div class="assess-criterion">{{ criterionB.letter }}. {{ criterionB.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.criteria_b, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item clicked" @click="getObjectivesFromCriteria(criterionC)">
            <div class="assess-criterion">{{ criterionC.letter }}. {{ criterionC.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.criteria_c, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item clicked" @click="getObjectivesFromCriteria(criterionD)">
            <div class="assess-criterion">{{ criterionD.letter }}. {{ criterionD.name_eng }}</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.criteria_d, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-sum">Оценка за ИР</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.summ_grades, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-form">Средняя текущая</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.form_grades, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
          <div class="assess-item">
            <div class="assess-final">Итоговая оценка</div>
            <div class="assess-mark">
              <div class="mark" v-for="(asper, index) in period.assessment_periods" :key="asper.id">
                {{ getMarkFromAssessment(student.assessment.final_grades, asper.number) }}
                <!-- <span v-if="++index != period.assessment_periods.length">- </span> -->
              </div>
            </div>
          </div>
        </div>
        <div class="achievements-wrapper">
          <div v-if="objectives.length">
            <div class="achievements-filter selected">
              <div>Показать предметные цели и уровни достижений по критерию <b>{{ this.currentCriterion.letter }}.{{ this.currentCriterion.name_eng }}</b> за:</div>
              <select class="form-select" name="level-subject" id="level-subject" v-model="currentYear">
                <option :value="null">Выберите уровень</option>
                <option v-for="lvl in levelSubject" :key="lvl.id" :value="lvl.id">{{ lvl.name_eng }}</option>
              </select>
            </div>
            <div class="accordion" :id="`accordion-${currentCriterion.id}`">
              <div class="accordion-item" v-for="objective in filteredObjectives" :key="objective.id">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-objective-${objective.id}`" aria-expanded="true" :aria-controls="`collapse-objective-${objective.id}`">
                    {{ objective.strand.letter_i }}. {{ objective.name_eng }}
                  </button>
                </h2>
                <div :id="`collapse-objective-${objective.id}`" class="accordion-collapse collapse" :data-bs-parent="`#accordion-${currentCriterion.id}`">
                  <div class="accordion-body">
                    <div v-if="objective.achievelevel.length">
                      <div class="achievement-item" v-for="ach in objective.achievelevel" :key="ach.id">
                        <div class="achievement-name">The student {{ ach.name_eng }}</div>
                        <div class="achievement-point">{{ ach.point - 1 }} - {{ ach.point }}</div>
                      </div>
                    </div>
                    <div v-else>Нет данных</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="student-criteria">
      <report-field-criteria id="student-criteria" :report="student.teacher_report" @save="fetchSaveReport" :avg_criteria="student.avg_assessment"
      :criteria="{ criterion_a: criterionA, criterion_b: criterionB, criterion_c: criterionC, criterion_d: criterionD }"/>
    </div>
    <div class="student-report">
      <report-field-text id="student-report" :student="student" :dataField="student.teacher_report" :generate="true"
      :criteria="{ criterion_a: criterionA, criterion_b: criterionB, criterion_c: criterionC, criterion_d: criterionD }" @save="fetchSaveReport"/>
    </div>
    <div class="student-events" v-if="student.teacher_report.text">
      <div class="events-title" data-bs-toggle="collapse" :href="`#collapse-events-${student.id}`" role="button" 
      aria-expanded="false" :aria-controls="`collapse-events-${student.id}`">Участие в мероприятиях</div>
      <report-field-blocks class="collapse" :id="`collapse-events-${student.id}`" :fieldData="student.teacher_report.events" 
      :fieldName="'events'" :defaultItem="defaultEvent" @save="fetchSaveReport">
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
            <input class="form-control my-1" type="text" v-model="item.data.title" placeholder="Название мероприятия">
            <div class="row">
              <div class="col-md">
                <select id="levels" class="form-select my-1" v-model="item.data.level">
                  <option :value="null">Выберите уровень</option>
                  <option v-for="(lvl, i) in levels" :key="i" :value="lvl.value">
                    {{ lvl.name }}
                  </option>
                </select>
              </div>
              <div class="col-md">
                <select id="types" class="form-select my-1" v-model="item.data.type_id">
                  <option :value="null">Выберите тип</option>
                  <option v-for="(type, i) in types" :key="i" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
            </div>
            <textarea class="form-control my-1" type="text" v-model="item.data.result" placeholder="Описание результатов"></textarea>
          </div>
        </template>
      </report-field-blocks>
    </div>
  </div>
</template>
  
<script>
import { mapGetters } from 'vuex';
import ReportFieldText from "@/components/assessment/ReportFieldText.vue";
import ReportFieldCriteria from "@/components/assessment/ReportFieldCriteria.vue";
import ReportFieldBlocks from "@/components/assessment/ReportFieldBlocks.vue";
import { getObjectives } from "@/hooks/unit/useObjective";
export default {
  name: 'ReportTeacherItem',
  components: {
    ReportFieldText, ReportFieldBlocks, ReportFieldCriteria
  },
  props: {
    student: {
      type: Object,
      default: {
        group: {},
        teacher_report: {},
        user: {},
        assessment: {
          criteria_a: {},
          criteria_b: {},
          criteria_c: {},
          criteria_d: {},
          sum_grades: {},
          form_grades: {},
          final_grades: {},
        }
      }
    },
    criteria: {
      type: Array,
      default: []
    },
    period: { Object },
    types: { 
      type: Array,
      default: [],
    },
    levels: { 
      type: Array,
      default: [],
    },
    levelSubject: {
      type: Array,
      default: [],
    }
  },
  setup(props) {
    const { objectives, fetchGetObjectives } = getObjectives();
    return {
      objectives, fetchGetObjectives
    }
  },
  data() {
    return {
      defaultEvent: {
        type_id: null,
        level: '0',
      },
      currentCriterion: null,
      currentYear: null
    }
  },
  methods: {
    getObjectivesFromCriteria(criterion) {
      this.currentCriterion = criterion;
      this.currentYear = null;
      this.fetchGetObjectives({ criterion: criterion.id })
    },
    getMarkFromAssessment(assess, period) {
      if (assess) {
        const assessMark = assess.find(item => item.period == period)
        if (assessMark) {
          return assessMark.mark || '0'
        } 
      }
      return 0
    },
    fetchSaveReport(data) {
      console.log('Сохранение репорта: ', data);
      let editReportStudents = { ...data }
      editReportStudents.student_id = this.student.id;
      editReportStudents.author_id = this.authUser.teacher.id;
      editReportStudents.id = this.student.teacher_report.id || null
      this.$emit('updateReport', editReportStudents);
    },
  },
  computed: {
    filteredObjectives() {
      console.log(this.currentYear)
      return this.objectives.filter(item => item.level.id == this.currentYear)
    },
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
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>
  
<style scoped>
.report-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
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
  margin-top: 15px;
  padding: 10px;
  border-radius: 10px;
}

/* .assess-title::after {
  content: '   \25BC';
} */
.student-assessment {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  column-gap: 5px;
}

.achievements-wrapper {
  flex-grow: 1;
  margin-bottom: 10px;
}
.achievements-filter {
  margin: 10px 0;
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 10px;
}
.achievements-filter select{
  margin-left: 10px;
  max-width: 200px;
}
.achievement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  column-gap: 10px;
}
.achievement-point {
  min-width: 100px;
  padding: 5px;
  border: 0.5px solid #a7a7a78a;
  text-align: center;
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
  row-gap: 5px;
}

.assess-item {
  display: flex;
  align-items: center;
  border: 0.5px solid var(--bs-secondary);
  padding: 5px 10px;
  border-radius: 10px;
}
.assess-item.clicked {
  cursor: pointer;
}
.assess-item.clicked:hover {
  background: var(--my-focus);
}
.assess-criterion {
  text-transform: uppercase;
  font-weight: 700;
}

.assess-mark {
  font-weight: 700;
  margin-left: auto;
  display: flex;
  column-gap: 5px;
}
.assess-mark .mark {
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  padding: 5px 5px;
  border-radius: 5px;
  background: var(--bs-secondary);
}

.student-criteria {
  margin-top: 10px;
}
.student-report {
  margin-top: 10px;
}
.events-title {
  margin-top: 10px;
  border-bottom: 0.5px solid #a7a7a78a;
}
.events-title:hover {
  font-weight: 700;
}
</style>