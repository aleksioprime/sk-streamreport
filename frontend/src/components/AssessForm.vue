<template>
  <form>
    <!-- Поле для ввода названия работы -->
    <div class="topPage">
      <label class="form-label">Название итоговой работы</label>
      <input class="form-control" id="title" type="text" v-model="summativeWork.title">
      <small ref="title_alert" class="alert-text"></small>
    </div>
    <!-- Поля для ввода поиска и выбора учителя -->
    <div class="row mt-3">
      <div class="col">
        <div class="d-flex align-items-center mb-2">
          <div class="me-3">Выберите учителя </div>
          <div class="flex-grow-1">
            <input id="teachers" class="form-control" type="text" v-model="searchTeachers"
              placeholder="Введите фамилию для поиска...">
          </div>
        </div>
        <div v-for="teacher in filteredTeachers" :key="teacher.id">
          <div class="form-check">
            <input ref="teacher" class="form-check-input" type="checkbox" :value="teacher.id"
              :id="'teacher-' + teacher.id" v-model="summativeWork.teachers_ids">
            <label class="form-check-label" :for="'teacher-' + teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
            </label>
          </div>
        </div>
      </div>
      <small ref="teachers_alert" class="alert-text"></small>
    </div>
    <!-- Выбор периода -->
    <div class="self">
      <label class="form-label">Период</label>
      <select id="period" class="form-select" v-model="summativeWork.period_id">
        <option :value="null">Выберите период</option>
        <option v-for="pr in periods" :key="pr.id" :value="pr.id">
          <span>{{ pr.number }} триместр ({{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }})</span>
        </option>
      </select>
      <small ref="period_alert" class="alert-text"></small>
    </div>
    <!-- Выбор предмета -->
    <div class="self">
      <label class="form-label">Предмет</label>
      <select id="subject" class="form-select" v-model="summativeWork.subject_id" @change="changeSubject">
        <option :value="null">Выберите предмет</option>
        <option v-for="sb in subjects" :key="sb.id" :value="sb.id">
          <span v-if="sb.group_ib">{{ sb.name_rus }} ({{ sb.group_ib.name_eng }})</span>
        </option>
      </select>
      <small ref="subject_alert" class="alert-text"></small>
    </div>
    <!-- Выбор юнита -->
    <div class="self">
      <label class="form-label">Юнит</label>
      <div v-if="unitsMYP.length">
        <select id="unit" class="form-select" v-model="summativeWork.unit_id" @change="changeUnit">
          <option :value="null">Выберите юнит</option>
          <option v-for="unit in unitsMYP" :key="unit.id" :value="unit.id">
            <span>{{ unit.title }} ({{ unit.class_year.year_rus }} класс)</span>
          </option>
        </select>
      </div>
      <div v-else>
        Выберите предмет, по которому есть созданные юниты
      </div>
      <small ref="unit_alert" class="alert-text"></small>
    </div>
    <!-- Выбор классов и даты итоговой работы -->
    <div class="self">
      <div>Даты итоговых работ</div>
      <div v-if="summativeWork.unit_id">
        <div class="my-2" v-if="summativeWork.groups.length">
          <table class="table border mb-0">
            <tr>
              <th class="text-center" style="width: 30%">Класс</th>
              <th class="text-center" style="width: 40%">Дата</th>
              <th class="text-center" style="width: 20%">Урок</th>
              <th class="text-center" style="width: 10%"></th>
            </tr>
            <tr v-for="(gr, i) in summativeWork.groups" :key="gr.id">
              <td class="p-2">{{ gr.group.class_year }}{{ gr.group.letter }} класс</td>
              <td>{{ new Date(gr.date).toLocaleDateString() }}</td>
              <td>{{ gr.lesson }}</td>
              <td>
                <button class="btn-table delete my-1" @click="deleteWorkGroupDate(gr.id)"></button>
              </td>
            </tr>
          </table>
        </div>
        <div v-else>
          Пока список пустой
        </div>
        <div class="row">
          <div class="col-sm">
            <select id="level" class="form-select" v-model="choisenWorkGroupDate.group">
              <option :value="null">Класс</option>
              <option v-for="gr in groups" :key="gr.id" :value="gr">
                {{ gr.class_year }}{{ gr.letter }} класс
              </option>
            </select>
          </div>
          <div class="col-sm-4">
            <input type="date" id="date" class="form-control" v-model="choisenWorkGroupDate.date">
          </div>
          <div class="col-sm-2">
            <input type="text" id="lesson" class="form-control" v-model="choisenWorkGroupDate.lesson">
          </div>
          <div class="col-sm-1 d-flex align-items-center me-3">
            <button class="img-btn-add ms-auto" @click="addWorkGroupDate" :disabled="!choisenWorkGroupDate.date || !choisenWorkGroupDate.lesson || !choisenWorkGroupDate.group"></button>
          </div>
        </div>          
      </div>
      <div v-else>
        Выберите юнит
      </div>
    </div>
    <!-- Выбор критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="criteriaMYP.length > 0 ">
          <div v-for="cr in criteriaMYP" :key="cr.id">
            <div class="form-check">
              <input ref="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="summativeWork.criteria_ids">
              <label class="form-check-label" :for="'criterion-' + cr.id">
                <b>{{ cr.letter }}:</b> {{ cr.name_eng }}
              </label>
            </div>
          </div>
        </div>
        <div v-else>Для выбора критериев оценки укажите дисциплину</div>  
        <small ref="criteria_alert" class="alert-text"></small>
      </div>
    </div>
  </form>
</template>

<script>
import { toRefs } from 'vue';
import { getUnitsMYP, getCriteriaMYP, getGroups } from "@/hooks/assess/getSumWorkData";

export default {
  props: {
    summativeWork: { type: Object },
    teachers: { type: Array },
    subjects: { type: Array },
    periods: { type: Array },
  },
  setup(props) {
    const { unitsMYP, getUnitsMYPData } = getUnitsMYP();
    const { criteriaMYP, getCriteriaData } = getCriteriaMYP();
    const { groups, getGroupsData } = getGroups();
    return {
      unitsMYP, getUnitsMYPData,
      criteriaMYP, getCriteriaData,
      groups, getGroupsData,
    }
  },
  data() {
    return {
      searchTeachers: null,
      choisenWorkGroupDate: { group: null },
    }
  },
  methods: {
    changeSubject(event) {
      console.log('Предмет выбран: ', event.target.value);
      this.getUnitsMYPData(event.target.value);
      this.getCriteriaData(event.target.value);
    },
    changeUnit(event) {
      console.log(event.target.value)
      let currentUnit = this.unitsMYP.find(item => item.id == event.target.value)
      this.getGroupsData(currentUnit.class_year.year_rus);
    },
    addWorkGroupDate(event) {
      event.preventDefault();
      this.summativeWork.groups.push(this.choisenWorkGroupDate);
    },
    editWorkGroupDate() {

    },
    deleteWorkGroupDate(i) {
      this.summativeWork.groups.splice(i, 1);
    },
  },
  mounted() {

  },
  watch: {

  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchteachers)
    filteredTeachers() {
      if (!this.searchTeachers) {
        return this.teachers.filter(teacher => this.summativeWork.teachers_ids.includes(teacher.id))
      }
      return this.teachers.filter((teacher) => {
        if (teacher.user) {
          return teacher.user.last_name.toLowerCase().includes(this.searchTeachers.toLowerCase()) || this.summativeWork.teachers_ids.includes(teacher.id)
        } else {
          return this.summativeWork.teachers_ids.includes(teacher.id)
        }
      })
    },
  }
}
</script>

<style scoped>
.topPage {
  padding-top: 0%;
}

.self {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.btn-table {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
}
.btn-table.edit {
  background: url('@/assets/img/item-edit.png') no-repeat 50% / 90%;
  margin-right: 5px;
}
.btn-table.delete {
  background: url('@/assets/img/item-delete.png') no-repeat 50% / 90%;
}
</style>
