<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
    <div class="row">
      <div class="col mb-2">
        <div>Период: <b>{{ currentPeriod.number }} {{ currentPeriod.type }}</b></div>
        <div>Предмет: <b>{{ currentSubject.name_rus }} ({{ currentSubject.group_ib.name_eng }})</b></div>
      </div>
      <div class="col-sm-4 mb-2">
        <select class="form-select" v-model="queryGroup">
          <option selected :value="null">{{ currentYear.year_rus }}-е классы</option>
          <option v-for="gr in currentGroups" :key="gr.id" :value="gr.id">{{ gr.class_year }}{{ gr.letter }} класс</option>
        </select>
      </div>
    </div>
    <div class="d-flex flex-column border p-2">
      <div v-for="(worksByUnit, unit) in groupedArrayData(sumWorks, ['unit'])" :key="unit.id">
        <b>{{ worksByUnit[0].unit.title }}</b>
        <div v-for="work in worksByUnit" :key="work.id">
          - {{ work.title }} (<span class="list-criteria" v-for="cr in work.criteria" :key="cr.id">{{ cr.letter }} </span>)
        </div>
      </div>
    </div>
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
        <template v-for="(st, index) in filteredStudentsByGroup" :key="st.id">
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
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'criterion_a') }}</div>
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.criterion_b">
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'criterion_b') }}</div>
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.criterion_c">
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'criterion_c') }}</div>
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.criterion_d">
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'criterion_d') }}</div>
            </td>
            <td class="uneditable">
              {{ calcSumAssessmentMarks(st) }}
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.summ_grade">
              <div class="table-text" @click="(event) => setEditField(event, st)" :title="getStudentCriteriaMarksResult(st)">{{ getMarkForStudent(st, 'summ_grade') }}</div>
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.form_grade">
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'form_grade') }}</div>
            </td>
            <td class="editable">
              <input type="text" class="table-input" v-model="currentAssess.final_grade">
              <div class="table-text" @click="(event) => setEditField(event, st)">{{ getMarkForStudent(st, 'final_grade') }}</div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { getPeriodAssess, getStudents, getSumWork, getGroupedArray, getAssessmentJournal, filterStudentsByGroup } from "@/hooks/assess/getPeriodAssess";

export default {
  name: 'AssessPeriodView',
  components: {

  },
  setup(props) {
    // Получение функции запроса данных студентов
    const { students, calcFinalCriteriaMarks, getStudentsData } = getStudents();
    const { queryGroup, filteredStudentsByGroup } = filterStudentsByGroup(students);
    // Получение функции запроса данных итоговых оценок студентов
    const { periodAssess, getPeriodAssessData } = getPeriodAssess();
    const { sumWorks, getSumWorkData } = getSumWork();
    const { groupedArrayData } = getGroupedArray();
    const { currentPeriod, currentYear, currentSubject, currentGroups, getAssssmentJournalData } = getAssessmentJournal();
    return {
      students, calcFinalCriteriaMarks, getStudentsData,
      queryGroup, filteredStudentsByGroup,
      periodAssess, getPeriodAssessData,
      sumWorks, getSumWorkData,
      groupedArrayData,
      currentPeriod, currentYear, currentSubject, currentGroups, getAssssmentJournalData
    }
  },
  data() {
    return {
      currentAssess: {},
    }
  },
  methods: {
    calcSumAssessmentMarks(student) {
      const assessment = this.periodAssess.find(item => item.student.id == student.id)
      if (assessment) {
        const listAssessmentMarks = [assessment.criterion_a, assessment.criterion_b, assessment.criterion_c, assessment.criterion_d]
        const sumMarks = listAssessmentMarks.reduce((acc, number) => acc + number, 0);
        const sumAll = listAssessmentMarks.filter(item => item != 0 && item != null).length * 8;
        if (sumAll) {
          return `${sumMarks}/${sumAll}`;
        }
      }
      return '-'
    },
    getStudentCriteriaMarksResult(student) {
      const assessment = this.periodAssess.find(item => item.student.id == student.id)
      if (assessment) {
        const listAssessmentMarks = [assessment.criterion_a, assessment.criterion_b, assessment.criterion_c, assessment.criterion_d]
        const sumMarks = listAssessmentMarks.reduce((acc, number) => acc + number, 0);
        const numMarks = listAssessmentMarks.filter(item => item != 0 && item != null).length;
        if (numMarks) {
          return this.calcFinalCriteriaMarks(sumMarks, numMarks);
        }
      }
      return '-'
    },
    getStudentFinalMarkPredict() {
      
    },
    getStudentFinalMarkResult() {

    },
    getMarkForStudent(student, field) {
      const criterionMark = this.periodAssess.find(item => item.student.id == student.id)
      if (criterionMark && criterionMark[field]) {
        return criterionMark[field]
      } else {
        return "-"
      }
    },
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
        const assess = this.periodAssess.find(item => item.student.id == student.id)
        if (assess) {
          this.setStudentGradeEdit(assess);
        } else {
          this.setStudentGradeAdd(student);
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
    setStudentGradeEdit(assess) {
      if (Object.keys(this.currentAssess).length) {
        console.log("Запрос на изменение данных: ", this.currentAssess);
        this.axios.put(`/assessment/periodassess/${assess.id}`, this.currentAssess).then((response) => {
          this.getPeriodAssessData({
            year: this.$route.params.id_year, 
            period: this.$route.params.id_period,
            subject: this.$route.params.id_subject
          });
          console.log('Оценка успешно обновлена');
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
    setStudentGradeAdd(student) {
      if (Object.keys(this.currentAssess).length) {
        this.currentAssess.student_id = student.id;
        this.currentAssess.subject_id = this.$route.params.id_subject;
        this.currentAssess.period_id = this.$route.params.id_period;
        this.currentAssess.year_id = this.$route.params.id_year;
        console.log("Запрос на Добавление данных: ", this.currentAssess);
        this.axios.post(`/assessment/periodassess`, this.currentAssess).then((response) => {
          this.getPeriodAssessData({
            year: this.$route.params.id_year, 
            period: this.$route.params.id_period,
            subject: this.$route.params.id_subject,
          });
          console.log('Оценка успешно выставлена');
        }).finally(() => {
          this.currentAssess = {};
        });
      }
    },
  },
  mounted() {
    this.getAssssmentJournalData({
      year: this.$route.params.id_year, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject
    })
    this.getSumWorkData({
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject,
      year: this.$route.params.id_year,
      teacher: this.authUser.teacher.id
    });
    this.getStudentsData({
      year: this.$route.params.id_year, 
      period: this.$route.params.id_period,
      subject: this.$route.params.id_subject
    }).finally(() => {
      this.getPeriodAssessData({
        year: this.$route.params.id_year, 
        period: this.$route.params.id_period,
        subject: this.$route.params.id_subject
      })
    });
    
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser']),
  }
}
</script>

<style scoped>
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
  background-color: #d9fafa;
  vertical-align: middle;
  text-align: center;
  min-width: 20px;
}
table .editable {
  background-color: #ffffff;
  font-weight: 500;
  text-align: center;
  min-width: 20px;
}
</style>