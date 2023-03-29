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
            <input class="form-check-input" type="radio" :value="teacher.id"
              :id="'teacher-' + teacher.id" v-model="summativeWork.teacher_id">
            <label class="form-check-label" :for="'teacher-' + teacher.id">
              {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
            </label>
          </div>
        </div>
      </div>
      <small ref="teacher_alert" class="alert-text"></small>
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
        <div class="my-2 border p-2">
          <table class="table mb-0" v-if="summativeWork.groups.length">
            <tr>
              <th class="ps-2" style="width: 30%">Класс</th>
              <th style="width: 40%">Дата</th>
              <th style="width: 20%">Урок</th>
              <th style="width: 10%"></th>
            </tr>
            <tr v-for="(gr, i) in summativeWork.groups" :key="gr.id">
              <td>
                <span v-if="findGroup(gr.group_id)">{{ findGroup(gr.group_id).class_year }}{{ findGroup(gr.group_id).letter }} класс</span>
              </td>
              <td>{{ new Date(gr.date).toLocaleDateString() }}</td>
              <td>{{ gr.lesson }}</td>
              <td>
                <div class="d-flex">
                  <div class="btn-table edit my-1" @click="editWorkGroupDate(gr.id)"></div>
                  <div class="btn-table delete my-1" @click="deleteWorkGroupDate(gr.id)"></div>
                </div>
              </td>
            </tr>
          </table>
          <div v-else>
            Пока список пустой
          </div>
        </div>
        <div class="mb-1">
          <span v-if="editDateGroup">Редактировать выбранную дату</span>
          <span v-else>Добавить новую дату</span>
        </div>
        <div class="border p-2">
          <div class="row">
            <div class="col-sm my-1">
              <select id="level" class="form-select" v-model="choisenWorkGroupDate.group_id">
                <option :value="null">Класс</option>
                <option v-for="gr in groups" :key="gr.id" :value="gr.id">
                  {{ gr.class_year }}{{ gr.letter }} класс
                </option>
              </select>
            </div>
            <div class="col-4 my-1">
              <input type="date" id="date" class="form-control" v-model="choisenWorkGroupDate.date">
            </div>
            <div class="col-2 my-1">
              <input type="text" id="lesson" class="form-control" v-model="choisenWorkGroupDate.lesson">
            </div>
            <div class="col-2 d-flex align-items-center me-3">
              <div v-if="editDateGroup" class="d-flex">
                <button class="btn-table apply ms-auto" @click="applyWorkGroupDate"></button>
                <button class="btn-table cancel ms-auto" @click="cancelWorkGroupDate"></button>
              </div>
              <button v-else class="img-btn-add ms-auto" @click="addWorkGroupDate" :disabled="!choisenWorkGroupDate.date || !choisenWorkGroupDate.lesson || !choisenWorkGroupDate.group_id"></button>
            </div>
          </div> 
        </div>         
        </div>
      <div v-else>
        Выберите юнит
      </div>
      <small ref="groups_alert" class="alert-text"></small>
    </div>
    <!-- Выбор критериев оценки -->
    <div class="row my-2">
      <div class="col">
        <div class="mb-2">Критерии оценки: </div>
        <div v-if="criteriaMYP.length > 0 ">
          <div v-for="cr in criteriaMYP" :key="cr.id">
            <div class="form-check">
              <input name="criteria" class="form-check-input" type="checkbox" :value="cr.id" :id="'criterion-' + cr.id" v-model="summativeWork.criteria_ids">
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
    editMode: { type: Boolean },
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
      choisenWorkGroupDate: { group_id: null },
      errorField: {},
      textAlert: {
        title: 'Введите название итоговой работы',
        teacher: 'Выберите учителя',
        period: 'Выберите учебный период',
        subject: 'Выберите предмет',
        unit: 'Выберите юнит',
        groups: 'Добавьте группы и даты итоговых работ',
        criteria: 'Выберите критерии оценки',
      },
      editDateGroup: false,
    }
  },
  methods: {
    changeSubject(event) {
      this.getUnitsMYPData(event.target.value);
      this.getCriteriaData(event.target.value);
    },
    changeUnit(event) {
      let currentUnit = this.unitsMYP.find(item => item.id == event.target.value)
      this.getGroupsData(currentUnit.class_year.year_rus);
    },
    addWorkGroupDate(event) {
      event.preventDefault();
      this.summativeWork.groups.push(this.choisenWorkGroupDate);
      this.choisenWorkGroupDate = { group_id: null };
    },
    editWorkGroupDate(id) {
      this.choisenWorkGroupDate = { ...this.summativeWork.groups.find(item => id == item.id) }
      this.editDateGroup = true;
    },
    deleteWorkGroupDate(id) {
      this.summativeWork.groups.splice(id, 1);
    },
    applyWorkGroupDate() {
      this.summativeWork.groups = this.summativeWork.groups.map(item => {
        if (this.choisenWorkGroupDate.id == item.id) {
          return this.choisenWorkGroupDate
        }
        return item
      });
      this.editDateGroup = false;
      this.choisenWorkGroupDate = { group_id: null };
    },
    cancelWorkGroupDate() {
      this.editDateGroup = false;
      this.choisenWorkGroupDate = { group_id: null };
    },
    findGroup(id) {
      return this.groups.find(item => id == item.id)
    },
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.summativeWork.title ? this.errorField.title = false : this.errorField.title = true;
      this.summativeWork.period_id ? this.errorField.period = false : this.errorField.period = true;
      this.summativeWork.subject_id ? this.errorField.subject = false : this.errorField.subject = true;
      this.summativeWork.teacher_id ? this.errorField.teacher = false : this.errorField.teacher = true;
      this.summativeWork.unit_id ? this.errorField.unit = false : this.errorField.unit = true;
      this.summativeWork.groups.length ? this.errorField.groups = false : this.errorField.groups = true;
      this.summativeWork.criteria_ids.length ? this.errorField.criteria = false : this.errorField.criteria = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('validForm', validate);
      this.validateForm();
    },
    // Валидация формы - проверка ошибок полей формы и вывод их в виде текста на форму
    validateForm() {
      for (let key in this.errorField) {
        if (this.$refs[`${key}_alert`]) {
          if (this.errorField[key]) {
            this.$refs[`${key}_alert`].innerText = this.textAlert[key];
          } else {
            this.$refs[`${key}_alert`].innerText = "";
          }
        }
      }
    },
  },
  mounted() {
    if (this.editMode) {
      console.log('Открытие формы в режиме редктирования');
      this.getUnitsMYPData(this.summativeWork.subject_id);
      this.getCriteriaData(this.summativeWork.subject_id);
      this.getGroupsData(this.summativeWork.unit.class_year.id);
    }
  },
  watch: {
  },
  computed: {
    // Переменная с данными отфильтрованных учителей по значению поля поиска по фамилии (searchteachers)
    filteredTeachers() {
      if (!this.searchTeachers) {
        return this.teachers.filter(teacher => this.summativeWork.teacher_id == teacher.id)
      }
      return this.teachers.filter((teacher) => {
        if (teacher.user) {
          return teacher.user.last_name.toLowerCase().includes(this.searchTeachers.toLowerCase()) || this.summativeWork.teacher_id == teacher.id
        } else {
          return this.summativeWork.teacher_id == teacher.id
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
.btn-table.apply {
  background: url('@/assets/img/btn-apply.png') no-repeat 50% / 90%;
  margin-right: 5px;
}
.btn-table.cancel {
  background: url('@/assets/img/btn-cancel.png') no-repeat 50% / 90%;
  margin-right: 5px;
}
.alert-text {
    color: red;
  }
</style>
