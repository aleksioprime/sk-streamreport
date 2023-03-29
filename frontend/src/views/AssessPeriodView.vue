<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
    <table>
            <thead class="thead-dark text-center">
              <tr>
                <th scope="col" class="text-center" rowspan="2">№</th>
                <th scope="col" rowspan="2" style="width: 50%" >ФИО студента</th>
                <th scope="col" colspan="4" style="width: 20%">Средние балы по критериям</th>
                <th scope="col" colspan="3" style="width: 10%" >Итоговая оценка</th>
                
              </tr>
              <tr>
                <th style="width: 5%">A</th>
                <th style="width: 5%">B</th>
                <th style="width: 5%">C</th>
                <th style="width: 5%">D</th>
                <th style="width: 10%">Сумма</th>
                <th style="width: 10%">Макс </th>
                <th style="width: 10%">Расчет </th>

              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">1</th>
                <td></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <th scope="row">2</th>
                <td></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <th scope="row">3</th>
                <td></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <th scope="row">4</th>
                <td></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td></td>
                <td></td>
                <td></td>
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
    width: 90%;
    height: auto;
    border-collapse: collapse;
    margin: auto auto;
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

</style>