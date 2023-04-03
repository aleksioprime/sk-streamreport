<template>
  <div>
    <div class="row">
      <div class="col">
        <h4>Студенты в списке класса</h4>
        <select class="form-select" multiple v-model="currentStudentsGroup">
          <option v-for="st in filterStudents" :key="st.id" :value="st">{{ st.user.last_name }} {{ st.user.first_name }}</option>
        </select>
      </div>
      <div class="col-2 d-flex flex-column justify-content-end">
        <button class="btn btn-success my-2" @click="addStudentsToWork" :disabled="!currentStudentsGroup.length">&#8594;</button>
        <button class="btn btn-danger my-2" @click="deleteStudentsFromWork" :disabled="!currentStudentsWork.length">&#8592;</button>
      </div>
      <div class="col">
        <h4>Студенты в журнале</h4>
        <select class="form-select" multiple v-model="currentStudentsWork">
          <option v-for="st in studentsWork" :key="st.id" :value="st.id">{{ st.user.last_name }} {{ st.user.first_name }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import { getStudents } from "@/hooks/assess/getSumWorkAssess";

export default {
  props: {
    studentsWork: {
      type: Array,
      default: () => []
    },
    year: {
      type: Object,
      default: {}
    }
  },
  setup(props) {
    // Получение функции запроса списка студентов
    const { students, getStudentsData } = getStudents();
    return {
      students, getStudentsData
    }
  },
  data() {
    return {
      currentStudentsWork: [],
      currentStudentsGroup: [],
    }
  },
  methods: {
    addStudentsToWork() {
      this.$emit('update:studentsWork', this.studentsWork.concat(this.currentStudentsGroup));
      this.currentStudentsGroup = [];
    },
    deleteStudentsFromWork() {
      this.$emit('update:studentsWork', this.studentsWork.filter(item => !this.currentStudentsWork.includes(item.id)));
      this.currentStudentsWork = [];
    },
  },
  mounted() {
    console.log('Текущий класс: ', this.year)
    this.getStudentsData({class: this.year.id});
  },
  computed: {
    filterStudents() {
      return this.students.filter(item => !this.studentsWork.map(item => item.id).includes(item.id))
    }
  },
  watch: {

  }
}
</script>

<style scoped></style>