<template>
  <form>
    <div class="modal-body">
      <div class="mt-2">
        <label class="form-label">Название итоговой работы</label>
        <input class="form-control" type="text">
      </div>

      <!-- учителя -->

      <div class="row mt-3">
        <div class="col">
          <div class="d-flex align-items-center mb-2">
            <div class="me-3">Выберите учителя </div>
            <div class="flex-grow-1"><input id="authors" class="form-control" type="text" v-model="searchAuthors"
                placeholder="Введите фамилию для поиска..."></div>
          </div>
          <div v-for="teacher in searchTeachers" :key="teacher.id">
            <div class="form-check">
              <input ref="teacher" class="form-check-input" type="checkbox" :value="teacher.id"
                :id="'teacher-' + teacher.id" v-model="modelValue.authors_ids"
                @change="updateFieldUnit('authors_ids', $event.target.value)">
              <label class="form-check-label" :for="'teacher-' + teacher.id">
                {{ teacher.user.first_name }} {{ teacher.user.middle_name }} {{ teacher.user.last_name }}
              </label>
            </div>
          </div>
        </div>
        <small ref="teacher_alert" class="alert-text"></small>
      </div>

      <div class="mt-2">
        <label class="form-label">Юнит</label>
        <select class="form-select">
          <option selected>Выберите юнит</option>
          <option value="1">Юнит 1</option>
          <option value="2">Юнит 2</option>
          <option value="3">Юнит 3</option>
        </select>
      </div>

      <div class="row mt-2">
        <div class="col-md">
          <label for="date" class="form-label">Дата проведения</label>
          <input type="date" id="date" class="form-control">
        </div>
        <div class="col-md">
          <label class="form-label">Период</label>
          <select class="form-select">
            <option selected>Выберите период</option>
            <option value="1">1 триместр</option>
            <option value="2">2 триместр</option>
            <option value="3">3 триместр</option>
          </select>
        </div>
      </div>


      <!-- Предметы -->



      <label class="form-label">Предмет</label>
      <select class="form-select">
        <option selected>Выберите учителя </option>
        <option value="1">Информатика</option>
        <option value="2">Математика</option>
        <option value="3"> История</option>
      </select>






      <div class="row">
        <div class="col-md">
          <label class="form-label">Классы</label>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
            <label class="form-check-label" for="flexCheckDefault">
              7A
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              7B
            </label>
          </div>


        </div>
        <div class="col-md">

          <label class="form-label">Критерии</label>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
            <label class="form-check-label" for="flexCheckDefault">
              A
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              B
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              C
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              D
            </label>
          </div>

        </div>
      </div>




    </div>

  </form>
</template>

<script>
import { toRefs } from 'vue'

export default {
  props: {

  },
  setup(props) {
    return {
    }
  },
  data() {
    return {

    }
  },
  methods: {

  },
  mounted() {

  },
  watch: {

  }
}
</script>

<style scoped></style>