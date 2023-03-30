<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
    <div class="info-block"> Предмет: Информатика </div>
    <div class="info-block">Период: 3 триместр </div>
    <div class="info-block">Юниты: *** </div>
    <div class="info-block">
    <div class="d-inline-flex"> 
      <select class="form-select">
        <option selected>Выберите класс</option>
        <option value="1">7а</option>
        <option value="2">7b</option>
      </select>
    </div>
  </div>



    <table>
      <thead class="thead-dark text-center">
        <tr>
          <th scope="col" class="text-center" rowspan="2">№</th>
          <th scope="col" rowspan="2" style="width: 50%">ФИО студента</th>
          <th scope="col" colspan="5" style="width: 20%">Средние балы по критериям</th>
          <th scope="col" colspan="4" style="width: 10%">Итоговая оценка</th>

        </tr>
        <tr>
          <th style="width: 5%">A</th>
          <th style="width: 5%">B</th>
          <th style="width: 5%">C</th>
          <th style="width: 5%">D</th>
          <th style="width: 10%">Сумма/Макс</th>
          <th style="width: 10%"> Оценка за ИКР </th>
          <th style="width: 10%">Среднее текущее </th>
          <th style="width: 10%">Итоговый расчет </th>
          <th style="width: 10%">Итоговая оценка </th>


        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">1</th>
          <td></td>
          <td>
            1
            2
            3
            Средняя:
            <input type="text" class="form-control">
          </td>
          <td>
            1
            2
            3
            Средняя:
            <input type="text" class="form-control">
          </td>
          <td>
            1
            2
            3
            Средняя:
            <input type="text" class="form-control">
          </td>
          <td>
            1
            2
            3
            Средняя:
            <input type="text" class="form-control">
          </td>
          <td></td>
          <td><input type="text" class="form-control"></td>
          <td></td>
          <td></td>
          <td><input type="text" class="form-control"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  name: 'AssessPeriodView',
  components: {

  },
  setup(props) {
    return {

    }
  },
  data() {
    return {
      modalAssessment: {}
    }
  },
  methods: {

  },
  mounted() {
    this.modalAssessment = new Modal(`#modalAssessment`, { backdrop: 'static' });
  },
  computed: {
  }
}
</script>

<style scoped>
table {
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
}

caption {
  margin-bottom: 10px;
  font-size: 18px;
}

.info-block {
  margin: 10px 0px 0px;

  
}
</style>