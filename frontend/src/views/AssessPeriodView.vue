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
      <thead class="thead-dark text-center align-middle">
        <tr>
          <td scope="col" rowspan="2">№</td>
          <td scope="col" rowspan="2" style="width: 50%">ФИО студента</td>
          <td scope="col" colspan="6" style="width: 20%">Оценка за итоговые работы</td>
          <td rowspan="2" style="width: 10%">Среднее текущее</td>
          <td rowspan="2" style="width: 10%">Итог</td>
        </tr>
        <tr>
          <td>A</td>
          <td>B</td>
          <td>C</td>
          <td>D</td>
          <td>Сумма</td>
          <td>Итог</td>
        </tr>
      </thead>
      <tbody>
        <template v-for="(st, index) in filteredStudentsByGroup" :key="st.id">
          <tr>
            <th scope="row" rowspan="2">{{ index + 1 }}</th>
            <td rowspan="2">{{ st.user.last_name }} {{ st.user.first_name }}</td>
            <td><div class="criterion-mark"><div class="criterion-mark-item" v-for="mark in getCriterionMarkForStudent(st, 'A')" :key="mark">{{ mark }}</div></div></td>
            <td><div class="criterion-mark"><div class="criterion-mark-item" v-for="mark in getCriterionMarkForStudent(st, 'B')" :key="mark">{{ mark }}</div></div></td>
            <td><div class="criterion-mark"><div class="criterion-mark-item" v-for="mark in getCriterionMarkForStudent(st, 'C')" :key="mark">{{ mark }}</div></div></td>
            <td><div class="criterion-mark"><div class="criterion-mark-item" v-for="mark in getCriterionMarkForStudent(st, 'D')" :key="mark">{{ mark }}</div></div></td>
            <td>{{ calcSumStudentMarks(st) }}</td>
            <td>{{ calcStudentCriteriaMarks(st) }}</td>
            <td rowspan="2"></td>
            <td></td>
          </tr>
          <tr>
            <td>
              <!-- <input type="text" class="input-table" v-model="criterionA"> -->
              <div>{{ getMarkForStudent(st, 'criterion_a') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="criterionB"> -->
              <div>{{ getMarkForStudent(st, 'criterion_b') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="criterionC"> -->
              <div>{{ getMarkForStudent(st, 'criterion_c') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="criterionD"> -->
              <div>{{ getMarkForStudent(st, 'criterion_d') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="sumGrade"> -->
              <div>{{ getMarkForStudent(st, 'sum_grade') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="formGrade"> -->
              <div>{{ getMarkForStudent(st, 'form_grade') }}</div>
            </td>
            <td>
              <!-- <input type="text" class="input-table" v-model="finalGrade"> -->
              <div>{{ getMarkForStudent(st, 'final_grade') }}</div>
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
    const { students, getStudentsData } = getStudents();
    const { queryGroup, filteredStudentsByGroup } = filterStudentsByGroup(students);
    // Получение функции запроса данных итоговых оценок студентов
    const { periodAssess, getPeriodAssessData } = getPeriodAssess();
    const { sumWorks, getSumWorkData } = getSumWork();
    const { groupedArrayData } = getGroupedArray();
    const { currentPeriod, currentYear, currentSubject, currentGroups, getAssssmentJournalData } = getAssessmentJournal();
    return {
      students, getStudentsData,
      queryGroup, filteredStudentsByGroup,
      periodAssess, getPeriodAssessData,
      sumWorks, getSumWorkData,
      groupedArrayData,
      currentPeriod, currentYear, currentSubject, currentGroups, getAssssmentJournalData
    }
  },
  data() {
    return {
      
    }
  },
  methods: {
    getCriterionMarkForStudent(student, letter) {
      const marks = student.workgroups.map(item => {
        const list_ = item.criteria_marks.filter(cm => cm.criterion.letter == letter).map(cm => cm.mark)
        return list_.toString()
      })
      return marks.filter(item => item).map(item => Number(item))
    },
    getAverage(numbers) {
      if (numbers.length) {
        const sum = numbers.reduce((acc, number) => acc + number, 0);
        const length = numbers.length;
        return sum / length;
      } 
      return 0;
    },
    getListStudentMarks(student) {
      const marksA = this.getCriterionMarkForStudent(student, 'A');
      const marksB = this.getCriterionMarkForStudent(student, 'B');
      const marksC = this.getCriterionMarkForStudent(student, 'C');
      const marksD = this.getCriterionMarkForStudent(student, 'D');
      const listMarks = [marksA, marksB, marksC, marksD]
      const listAverageMarks = listMarks.map(item => this.getAverage(item))
      return listAverageMarks
    },
    calcSumStudentMarks(student) {
      const listAverageMarks = this.getListStudentMarks(student);
      const sumMarks = listAverageMarks.reduce((acc, number) => acc + number, 0);
      const sumAll = listAverageMarks.filter(item => item != 0).length * 8
      if (sumAll) {
        return `${sumMarks}/${sumAll}`;
      }
      return '-'
    },
    calcStudentCriteriaMarks(student) {
      const grades = {1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28]};
      const listMarks = this.getListStudentMarks(student);
      const sumMarks = listMarks.reduce((acc, number) => acc + number, 0);
      const numMarks = listMarks.filter(item => item != 0).length
      if (!numMarks) {
        return '-'
      } else if (sumMarks >= grades[numMarks][2]) {
        return 5
      } else if (sumMarks < grades[numMarks][2] && sumMarks >= grades[numMarks][1]) {
        return 4
      } else if (sumMarks < grades[numMarks][1] && sumMarks >= grades[numMarks][0]) {
        return 3
      } else if (sumMarks < grades[numMarks][0] && sumMarks > 0) {
        return 2
      } else {
        return '-'
      }
    },
    getMarkForStudent(student, field) {
      const criterionMark = this.periodAssess.find(item => item.student.id == student.id)
      if (criterionMark) {
        return criterionMark[field]
      } else {
        return "-"
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
/* table {
  width: 100%;
  height: auto;
  border-collapse: collapse;
  margin: 20px 0px 8px;
}

td {
  padding: 5px;
  padding-right: 10px;
  border: 1px solid black;
}

th {
  padding: 10px;
  border: 1px solid black;
} */
.criterion-mark {
  display: flex;
}
.criterion-mark-item {
  padding: 3px;
  border-radius: 3px;
  background: #d7f1f1;
}
.criterion-mark-item:not(:last-of-type) {
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

.input-table {
  background: #d7f1f1;
}
</style>