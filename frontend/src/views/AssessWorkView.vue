<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за итоговую работу</template>
    </base-header>
    <modal-class @save="saveClassModal" @cancel="hideClassModal" :modalTitle="modalTitleClass">
      <assess-work-form v-if="completeLoadWorkGroup" v-model:studentsWork="studentsWork" :year="workGroup.group"/>
    </modal-class>
    <div class="info">
      <div>{{ workGroup.work.title }}</div>
      <div v-if="workGroup.work.unit">{{ workGroup.work.unit.title }}</div>
      <div v-if="workGroup.work.groups">{{ workGroup.group.class_year }}{{ workGroup.group.letter }} класс</div>
    </div>
    <button class="btn btn-primary mt-2" @click="showClassModal">Изменить список группы</button>
    <div class="tools" ref="activeInput">

    </div>
    <div v-if="workGroup.students.length">
      <!-- Таблица оценок выбранного итоговой работы и класса -->
      <table class="table table-sm table-bordered mt-3 mark-table">
        <thead class="thead-dark text-center">
          <tr>
            <th rowspan="2" style="width: 5%">№</th>
            <th rowspan="2" style="width: 50%">ФИО студента</th>
            <th :colspan="workGroup.work.criteria.length">Баллы по критериям</th>
            <th rowspan="2" style="width: 10%">Сумма</th>
            <th rowspan="2" style="width: 10%">Расчёт</th>
            <th rowspan="2" style="width: 10%">Оценка</th>
          </tr>
          <tr>
            <th style="width: 5%" v-for="cr in workGroup.work.criteria" :key="cr.id">{{ cr.letter }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(assess, index) in workGroup.students" :key="assess.id">
            <td class="text-center">{{ index + 1 }}</td>
            <td>{{ assess.student.user.last_name }} {{ assess.student.user.first_name }}</td>
            <td v-for="cr in workGroup.work.criteria" :key="cr.id" class="criterion">
              <input type="text" class="input-table" v-model="markCriterion.mark">
              <div @click="(event) => setEditField(event, assess, cr)">{{ getMarkForStudent(cr.id, assess.criteria_marks) }}</div>
            </td>
            <td class="text-center">
              <b>{{ calcSumStudentMarks(assess.criteria_marks) }}</b>/{{ calcMaxStudentMarks(workGroup.work.criteria) }}
            </td>
            <td class="text-center">{{ calcStudentMarks(assess.criteria_marks, workGroup.work.criteria) }}</td>
            <td class="text-center grade">
              <input type="text" class="input-table" v-model="currentWorkAssess.grade">
              <div class="text-table" @click="(event) => setEditField(event, assess)">{{ assess.grade || "-" }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="alert alert-danger mt-3" role="alert">
        В этом классе пока нет студентов для оценки!
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import AssessWorkForm from "@/components/AssessWorkForm.vue"
import { getWorkGroup } from "@/hooks/assess/getSumWorkAssess"

export default {
  name: 'AssessWorkView',
  components: {
    AssessWorkForm,
  },
  setup(props) {
    // Получение функции запроса данных итоговой работы
    const { workGroup, getWorkGroupData } = getWorkGroup();
    return {
      workGroup, getWorkGroupData,
    }
  },
  data() {
    return {
      modalClass: {},
      currentWorkAssess: {},
      markCriterion: {},
      modalTitleClass: null,
      studentsWork: [],
      completeLoadWorkGroup: false,
    }
  },
  methods: {
    showClassModal() {
      this.modalTitleClass = "Изменение списка группы";
      this.getStudentsWork();
      this.modalClass.show();
    },
    saveClassModal() {
      const dataStudentsWork = {
        "students": this.studentsWork.map(item => { return {'student_id': item.id} }),
      }
      console.log('Отправка запроса на добавление студентов в журнал: ', dataStudentsWork);
      this.axios.put(`/assessment/workgroup/${this.$route.params.id}`, dataStudentsWork).then((response) => {
          console.log('Список студентов успешно изменён');
          this.getWorkGroupData(this.$route.params.id);
        }).finally(() => {
          console.log('Запрос завершён');
        });
      this.hideClassModal();
    },
    hideClassModal() {
      this.modalClass.hide();
    },
    getMarkForStudent(criterion, marks) {
      const criterionMark = marks.find(item => item.criterion.id == criterion)
      if (criterionMark) {
        return criterionMark.mark
      } else {
        return "-"
      }
    },
    calcSumStudentMarks(marks) {
      return marks.reduce((sum, item) => sum + item.mark, 0);
    },
    calcMaxStudentMarks(criteria) {
      return criteria.length * 8
    },
    calcStudentMarks(marks, criteria) {
      const grades = {1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28]};
      const sum = marks.reduce((sum, item) => sum + item.mark, 0);
      const numMarks = criteria.length
      if (sum >= grades[numMarks][2]) {
        return 5
      } else if (sum < grades[numMarks][2] && sum >= grades[numMarks][1]) {
        return 4
      } else if (sum < grades[numMarks][1] && sum >= grades[numMarks][0]) {
        return 3
      } else if (sum < grades[numMarks][0] && sum > 0) {
        return 2
      } else {
        return '-'
      }
    },
    setEditField(event, assess, criterion) {
      let textElement = event.target
      let inputElement = event.target.parentElement.firstChild
      inputElement.value = textElement.textContent
      textElement.style.display = 'none';
      inputElement.style.display = 'block';
      inputElement.focus();
      inputElement.select();
      // Функция для сохранения изменённых данных в ячейке
      const saveData = () => {
        if (criterion) {
          this.setStudentCriteriaMark(assess, criterion);
        } else {
          this.setStudentGrade(assess);
        }
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
      }
      // Функция для отмены сохранения изменённых данных в ячейке
      const cancelData = () => {
        textElement.style.display = 'block';
        inputElement.style.display = 'none';
        this.currentWorkAssess = {};
        this.markCriterion = {};
      }
      // Привязка функций к событиям потери фокуса и нажатию на Enter
      inputElement.onblur = cancelData;
      inputElement.onkeypress = (e) => {
        if (e.key === "Enter") { saveData() }
      };
    }, 
    setStudentGrade(assess) {
      if (Object.keys(this.currentWorkAssess).length) {
        if (this.currentWorkAssess.grade > 5) {
          this.currentWorkAssess.grade = 5
        } else if (this.currentWorkAssess.grade < 0) {
          this.currentWorkAssess.grade = 0
        }
        console.log("Запрос на изменение данных: ", this.currentWorkAssess);
        this.axios.put(`/assessment/workassess/${assess.id}`, this.currentWorkAssess).then((response) => {
          this.getWorkGroupData(this.$route.params.id);
          console.log('Оценка успешно обновлена');
        }).finally(() => {
          this.currentWorkAssess = {};
        });
      }
    },
    setStudentCriteriaMark(assess, criterion) {
      if (Object.keys(this.markCriterion).length) {
        this.markCriterion.criterion_id = criterion.id;
        const assessMark = { ...assess.criteria_marks.find(item => item.criterion.id == criterion.id) };
        if (assessMark) { 
          this.markCriterion.id = assessMark.id;
        }
        if (this.markCriterion.mark > 8) {
          this.markCriterion.mark = 8
        } else if (this.markCriterion.mark < 0) {
          this.markCriterion.mark = 0
        } else {
          this.markCriterion.mark = Number(this.markCriterion.mark)
        }
        const dataMarkCriterion = {
          "criteria_marks": [ this.markCriterion ],
        }
        console.log("Запрос на изменение данных: ", dataMarkCriterion);
        this.axios.put(`/assessment/workassess/${assess.id}`, dataMarkCriterion).then((response) => {
          this.getWorkGroupData(this.$route.params.id);
          console.log('Оценка успешно обновлена');
        }).finally(() => {
          this.markCriterion = {};
        });
      }
    },
    getStudentsWork() {
      this.studentsWork = this.workGroup.students.map(item => item.student)
    },
  },
  mounted() {
    this.getWorkGroupData(this.$route.params.id).finally(() => {
      this.getStudentsWork();
      this.completeLoadWorkGroup = true;
    });
    this.modalClass = new Modal(`#modalClass`, { backdrop: 'static' });
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style scoped>
.mark-table .criterion{
  text-align: center;
  max-width: 20px;
  background: #d7f1f1;
  
}
.mark-table .grade{
  text-align: center;
  max-width: 20px;
  background: #d7f1f1;
}
.mark-table .cell-edit {
  background: #000;
}
.input-table {
  width: 100%;
  border: none;
  display: none;
}
.text-table {
  cursor: pointer;
}

</style>