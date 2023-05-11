<template>
  <div>
    <base-header>
      <template v-slot:link><div @click="$router.push(`/assessment/group`)" class="link-back">Вернуться назад</div></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
    <div class="row">
      <div class="col mb-2">
        <div>Период: <b>{{ currentPeriod.number }} {{ currentPeriod.type }}</b></div>
        <div>Класс: <b>{{ currentGroup.class_year }}{{ currentGroup.letter }}</b> (Наставник: {{ currentGroup.mentor.user.last_name }} {{ currentGroup.mentor.user.first_name }} {{ currentGroup.mentor.user.middle_name }})</div>
        <div>Предмет: <b>{{ currentSubject.name_rus }} ({{ currentSubject.group_ib.name_eng }})</b></div>
      </div>
    </div>
    <div class="d-flex flex-column border p-2">
      <div v-for="(worksByUnit, unit) in groupedArrayData(summativeWorks, ['unit'])" :key="unit.id">
        <b>{{ worksByUnit[0].unit.title }}</b>
        <div v-for="work in worksByUnit" :key="work.id">
          - {{ work.title }} (<span class="list-criteria" v-for="cr in work.criteria" :key="cr.id">{{ cr.letter }} </span>)
        </div>
      </div>
    </div>
    <div v-if="!isStudentsAssessmentLoading">
      <table class="table table-sm table-bordered mt-2 table-responsive w-100">
        <thead class="text-center align-middle">
          <tr>
            <td scope="col" rowspan="2">№</td>
            <td scope="col" rowspan="2">ФИО студента</td>
            <td scope="col" colspan="6">Оценка за итоговые работы</td>
            <td rowspan="2" style="width: 25px">Среднее текущее</td>
            <td rowspan="2" style="width: 25px">Итог</td>
          </tr>
          <tr>
            <td>A</td>
            <td>B</td>
            <td>C</td>
            <td>D</td>
            <td>Сумма</td>
            <td style="width: 25px">Итог</td>
          </tr>
        </thead>
        <tbody>
          <template v-for="(st, index) in studentsAssessment" :key="st.id">
            <tr>
              <th scope="row" rowspan="2">{{ index + 1 }}</th>
              <td rowspan="2">{{ st.user.last_name }} {{ st.user.first_name }}</td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-a" v-for="mark in st.calcCriteriaA" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-b" v-for="mark in st.calcCriteriaB" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-c" v-for="mark in st.calcCriteriaC" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable"><div class="criterion-mark"><div class="criterion-mark item cr-d" v-for="mark in st.calcCriteriaD" :key="mark">{{ mark }}</div></div></td>
              <td class="uneditable">{{ st.sumCriteria }}/{{ st.allCriteria }}</td>
              <td class="uneditable">{{ st.criteriaFinalMark }}</td>
              <td class="uneditable"></td>
              <td class="uneditable">{{ st.finalGrade }}</td>
            </tr>
            <tr>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_a">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_a || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_b">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_b || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_c">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_c || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.criterion_d">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.criterion_d || '-' }}</div>
              </td>
              <td class="uneditable" :title="st.periodassess.prediction_criterion">
                <div v-if="st.periodassess.count_criterion">{{ st.periodassess.summ_criterion }}/{{ st.periodassess.count_criterion * 8 }}</div>
                <div v-else>-</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.summ_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.summ_grade || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.form_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.form_grade || '-' }}</div>
              </td>
              <td class="editable">
                <input type="text" class="table-input" v-model="currentAssess.final_grade">
                <div class="table-text" @click="(event) => setEditField(event, st)">{{ st.periodassess.final_grade || '-' }}</div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
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
import { mapGetters } from 'vuex';
import { getAssessmentJournal, getSummativeWork, getStudentsAssessment } from "@/hooks/assess/usePeriodAssessment";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'AssessPeriodView',
  components: {

  },
  setup(props) {
    const { studentsAssessment, calcFinalCriteriaMarks, isStudentsAssessmentLoading, fetchGetStudentsAssessment } = getStudentsAssessment();
    const { summativeWorks, fetchGetSummativeWork } = getSummativeWork();
    const { groupedArrayData } = getGroupedArray();
    const { currentPeriod, currentSubject, currentGroup, currentClassYear, fetchGetAssessmentJournal } = getAssessmentJournal();
    return {
      studentsAssessment, calcFinalCriteriaMarks, isStudentsAssessmentLoading, fetchGetStudentsAssessment,
      summativeWorks, fetchGetSummativeWork,
      groupedArrayData,
      currentPeriod, currentSubject, currentClassYear, currentGroup, fetchGetAssessmentJournal,
    }
  },
  data() {
    return {
      currentAssess: {},
    }
  },
  methods: {
    setEditField(event, student) {
      let textElement = event.target
      let inputElement = event.target.parentElement.firstChild
      inputElement.value = textElement.textContent
      textElement.style.display = 'none';
      inputElement.style.display = 'block';
      inputElement.focus();
      inputElement.select();
      // Функция для сохранения изменённых данных в ячейке
      const saveData = () => {
        if (student.periodassess.id) {
          this.setStudentGradeEdit(student.periodassess.id);
        } else {
          this.setStudentGradeAdd(student.id);
        }
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
      }
      // Функция для отмены сохранения изменённых данных в ячейке
      const cancelData = () => {
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
        this.currentAssess = {};
      }
      // Привязка функций к событиям потери фокуса и нажатию на Enter
      inputElement.onblur = cancelData;
      inputElement.onkeypress = (e) => {
        if (e.key === "Enter") { saveData() }
        if (e.key === "Escape") { cancelData() }
      };
    },
    setStudentGradeEdit(periodassess_id) {
      if (Object.keys(this.currentAssess).length) {
        console.log("Запрос на изменение данных: ", this.currentAssess);
        this.axios.put(`/assessment/periodassess/${periodassess_id}`, this.currentAssess).then((response) => {
          this.fetchGetStudentsAssessment({
            group: this.$route.params.id_group, 
            period: this.$route.params.id_period,
            subject: this.$route.params.id_subject,
            class_year: this.currentClassYear.id,
          });
          console.log('Оценка успешно обновлена');
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
    setStudentGradeAdd(student_id) {
      if (Object.keys(this.currentAssess).length) {
        this.currentAssess.student_id = student_id;
        this.currentAssess.subject_id = this.$route.params.id_subject;
        this.currentAssess.period_id = this.$route.params.id_period;
        this.currentAssess.year_id = this.currentClassYear.id;
        console.log("Запрос на Добавление данных: ", this.currentAssess);
        this.axios.post(`/assessment/periodassess`, this.currentAssess).then((response) => {
          this.fetchGetStudentsAssessment({
            group: this.$route.params.id_group, 
            period: this.$route.params.id_period,
            subject: this.$route.params.id_subject,
            class_year: this.currentClassYear.id,
          });
          console.log('Оценка успешно выставлена');
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
  },
  mounted() {
    this.fetchGetAssessmentJournal({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject
    })
    this.fetchGetSummativeWork({
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
      group: this.$route.params.id_group,
      teacher: this.authUser.teacher.id
    });
    this.fetchGetStudentsAssessment({
      group: this.$route.params.id_group, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
      class_year: this.currentClassYear.id,
    });
    
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser']),
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
.link-back {
  cursor: pointer;
}
.criterion-mark {
  display: flex;
}
.criterion-mark.item {
  padding: 3px;
  border-radius: 3px;
}
.item.cr-a{
  background: #c7735e;
  color: #fff;
}
.item.cr-b{
  background: #c7c55e;
  color: #fff;
}
.item.cr-c{
  background: #2cb801;
  color: #fff;
}
.item.cr-d{
  background: #ae5ec7;
  color: #fff;
}
.criterion-mark.item:not(:last-of-type) {
  margin-right: 3px;
}
.list-criteria {
  font-weight: 700;
}.list-criteria:not(:last-of-type)::after {
  content: ', '
}
.caption {
  margin-bottom: 10px;
  font-size: 18px;
}

.info-block {
  margin: 10px 0px 0px;
}

.table-input {
  border: none;
  display: none;
  width: 25px;
}
.table-text {
  cursor: pointer;
}
table .uneditable {
  background-color: #f7f7f7;
  vertical-align: middle;
  text-align: center;
  min-width: 20px;
}
table .editable {
  background-color: #ffffff;
  font-weight: 500;
  text-align: center;
  min-width: 20px;
  /* cursor: pointer; */
}
/* table .editable:hover {
  background-color: #fffcfc;
} */
</style>