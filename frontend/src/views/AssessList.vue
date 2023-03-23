<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговые работы</template>
    </base-header>
    <div class="tools">
      <div class="my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
          <option v-for="(study, i) in studyYears" :key="i" :value="study">
              {{ study.name }} учебный год
          </option>
        </select>
      </div>
      <button type="button" class="btn btn-primary ms-auto mb-2 w-100" @click="showAssessModalAdd">
        Cоздать итоговую работку
      </button>
    </div>
    
    <!-- Модальное окно добавления/редактирования/удаления итоговой работы -->
    <modal-assess :modalTitle="modalTitle" @cancel="hideAssessModal">
      <template v-slot:body>
        <!-- Форма добавления/редактирования итоговой работы -->
        <assess-form v-model="currentAssess" v-if="flagAssess.add || flagAssess.edit"/>
        <!-- Текст удаления итоговой работы -->
        <div v-if="flagAssess.delete">Вы действительно хотите удалить эту итоговую работу?</div>
      </template>
    </modal-assess>
    <!-- Выбор периодов обучения -->
    <div class="period">
      <div class="period-item" :class="[currentPeriod == pr ? 'period-select' : '']" 
        v-for="pr in periods" :key="pr.id" @click="refreshSumWorkBySubject(pr)">
        <div class="period-item-title">{{ pr.number }} триместр</div>
        <div class="period-item-year">
          <span v-for="(cy, index) in pr.class_year" :key="cy.id">{{ cy.year_rus }}<span v-if="index != pr.class_year.length - 1">, </span> </span> класс
        </div>
        <div class="period-item-date">{{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }}</div>
      </div>
    </div>
    <!-- Вывод итоговых работ учителя, сгруппированных по предметам -->
    <div v-if="Object.keys(groupedSumWorks).length !== 0" class="sumworks">
      <div v-for="(sumworks, subject) in groupedSumWorks" :key="subject">
        <div class="sumworks-subject" v-if="getSubject(subject)">{{ getSubject(subject).name_rus }}</div>
        <div class="sumworks-item" v-for="sw in sumworks" :key="sw.id">
          <div class="title">
            <div class="text">{{ sw.title }}</div>
            <div class="tools">
              <div class="btn edit"></div>
              <div class="btn delete"></div>
            </div>
          </div>
          <div class="unit">Юнит: {{ sw.unit.title }}</div>
          <div class="assessment">
            <div class="text">Оценки:</div>
            <div v-if="sw.groups.length">
              <div class="groups" v-for="gr in sw.groups" :key="gr.id">
                <div class="group">{{ gr }}</div>
              </div>
            </div>
            <div v-else>Не выбраны классы</div>
          </div>
          
        </div>
      </div>
    </div>
    <div v-else class="sumworks-empty">
      Нет данных
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import AssessForm from "@/components/AssessForm.vue";
import { getSumWork, getTeachers, getGrades, getSubjects, getPeriods, getStudyYears } from "@/hooks/assess/getSumWorkData";

export default {
  name: 'Assessment',
  components: {
    AssessForm,
  },
  setup(props) {
    const { sumWorks, getSumWorkData } = getSumWork()
    const { grades, getGradesData } = getGrades()
    const { teachers, getTeachersData } = getTeachers()
    const { subjects, getSubjectsData } = getSubjects()
    const { periods, currentPeriod, getPeriodsData } = getPeriods()
    const { studyYears, currentStudyYear, getStudyYearsData } = getStudyYears()
    return {
      sumWorks, getSumWorkData,
      grades, getGradesData,
      teachers, getTeachersData,
      subjects, getSubjectsData,
      periods, currentPeriod, getPeriodsData,
      studyYears, currentStudyYear, getStudyYearsData
    }
  },
  data() {
    return {
      modalAssess: {},
      modalTitle: '',
      flagAssess: {
        add: false,
        edit: false,
        delete: false,
      },
      currentAssess: {},
    }
  },
  methods: {
    hideAssessModal() {
      this.modalAssess.hide();
    },
    showAssessModalAdd() {
      this.modalTitle = 'Создание итоговой работы';
      this.modalAssess.show();
      this.flagAssess.add = true;
    },
    showAssessModalEdit() {
      this.modalTitle = 'Редактирование итоговой работы';
      this.modalAssess.show();
      this.flagAssess.edit = true;
    },
    showAssessModalDelete() {
      this.modalTitle = 'Удаление итоговой работы';
      this.modalAssess.show();
      this.flagAssess.delete = true;
    },
    assessCreate() {
      console.log("Запрос на создание итоговой работы");
    },
    assessEdit() {
      console.log("Запрос на изменение итоговой работы");
    },
    assessDelete() {
      console.log("Запрос на удаление итоговой работы");
    },
    getSubject(id) {
      return this.subjects.find(item => item.id == id); 
    },
    // Обновление итоговых работ при выборе периода
    refreshSumWorkBySubject(pr) {
      this.currentPeriod = pr;
      this.getSumWorkData({period: pr.id});
    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalAssess = new Modal('#modalAssess', { backdrop: 'static' });
    this.getStudyYearsData();
    this.getSubjectsData();
    this.getPeriodsData(this.currentStudyYear);
    this.getSumWorkData({period: this.currentStudyYear.id});
  },
  computed: {
    // преобраование массива итоговых работ в группированный по предмету объект массивов
    groupedSumWorks() {
      let groupedObject = this.sumWorks.reduce((acc, obj) => {
        const property = obj.subject.id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
  }
}
</script>

<style>
.period {
  display: flex;
  justify-content: center;
  margin: 10px;
}
.period-item {
  padding: 10px;
  cursor: pointer;
  border: 1px solid #33cccc;
  border-radius: 5px;
  flex-grow: 1;
  text-align: center;
}
.period-item:not(:last-of-type) {
  margin-right: 5px;
}
.period-item:hover {
  background: #33cccc;
  color: #ffffff;
}
.period-item-title {
  font-weight: 500;
}
.period-item-date {
  font-size: 0.7rem;
}
.period-select {
  background: #1e7979;
  color: #ffffff;
}
.sumworks {
  display: flex;
  flex-direction: column;
  padding: 10px;
}
.sumworks-subject {
  font-weight: 700;
  padding: 10px;
  background: #b9c7c7;
}
.sumworks-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #33cccc;
}
.sumworks-item .title {
  display: flex;
}
.sumworks-item .title .text {
  color: #1e7979;
  font-weight: 700;
}
.sumworks-item .tools {
  display: flex;
  margin-left: auto;
}
.sumworks-item .tools .btn {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
}
.btn.edit {
  background: url('@/assets/img/item-edit.png') no-repeat 50% / 90%;
  margin-right: 5px;
}
.btn.delete {
  background: url('@/assets/img/item-delete.png') no-repeat 50% / 90%;
}
.sumworks-item .unit {
  display: flex;
}
.sumworks-item .assessment {
  display: flex;
}
.sumworks-item .assessment .text {
  margin-right: 5px;
}
.sumworks-item .assessment .groups {
  display: flex;
}
.sumworks-empty 
{
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 30vh;
}
</style>