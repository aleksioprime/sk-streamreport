<template>
  <div>
    <base-header>
      <template v-slot:header>Мои итоговые работы</template>
    </base-header>
    <div class="tools">
      <div class="my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
          <option v-for="(study, i) in studyYears" :key="i" :value="study">
              {{ study.name }} учебный год
          </option>
        </select>
      </div>
      <button type="button" class="btn btn-primary ms-auto mb-2 w-100" @click="showSumWorkModalAdd">
        Cоздать итоговую работу
      </button>
    </div>
    <!-- Модальное окно добавления/редактирования/удаления итоговой работы -->
    <modal-assess :modalTitle="modalTitle" :flagAssess="flagAssess" 
      @create="sumWorkCreate" @delete="sumWorkDelete" @update="sumWorkEdit" @cancel="hideSumWorkModal">
      <template v-slot:body>
        <!-- Форма добавления/редактирования итоговой работы -->
        <assess-form v-model:summativeWork="currentAssess" v-if="flagAssess.add || flagAssess.edit" :teachers="teachers"
          :subjects="subjects" :periods="periods" @validForm="validFormResult" ref="assessmentForm" :editMode="formEditMode"/>
        <!-- Текст удаления итоговой работы -->
        <div v-if="flagAssess.delete" >
          <div class="mb-2">Вы действительно хотите удалить эту итоговую работу?</div>
          <div class="border p-2">
            <b>{{ currentAssess.title }}</b><br>
            <div>{{ currentAssess.unit.title }}</div>
            <div v-for="gr in currentAssess.groups" :key="gr.id">{{ gr.group.class_year }}{{ gr.group.letter }} класс - {{ new Date(gr.date).toLocaleDateString() }}</div>
          </div>
        </div>
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
    <div v-if="Object.keys(groupedSumWorks(sumWorks, ['subject'])).length !== 0" class="sumworks">
      <div v-for="(worksBySubject, subject) in groupedSumWorks(sumWorks, ['subject'])" :key="subject">
        <div class="sumworks-subject" v-if="getSubject(subject)">{{ getSubject(subject).name_rus }}</div>
        <div v-for="(worksByYear, year) in groupedSumWorks(worksBySubject, ['unit', 'class_year'])" :key="year">
          <div class="sumworks-grouped">
            <div class="sumworks-year">
              <div class="title" v-if="getGrade(year)">{{ getGrade(year).year_rus }} классы</div>
              <div class="sumassess" @click="$router.push(`/assessment/year/${year}/period/${currentPeriod.id}/subject/${subject}`)">Итоговые оценки</div>
            </div>
            <assess-item v-for="sumwork in worksByYear" :key="sumwork.id" :sumwork="sumwork" @editWork="showSumWorkModalEdit(sumwork.id)" @deleteWork="showSumWorkModalDelete(sumwork.id)"/>
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
import { mapGetters } from 'vuex';
import AssessForm from "@/components/AssessForm.vue";
import AssessItem from "@/components/AssessItem.vue";
import { getSumWork, getTeachers, getGrades, getSubjects, getPeriods, getStudyYears } from "@/hooks/assess/getSumWorkData";

export default {
  name: 'Assessment',
  components: {
    AssessForm, AssessItem
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
      flagAssess: {},
      currentAssess: {
        teacher_id: null,
        criteria_ids: [],
        groups: [],
        subject_id: null,
        unit_id: null,
        period_id: null,
      },
      validForm: false,
      formEditMode: false,
    }
  },
  methods: {
    hideSumWorkModal() {
      this.modalAssess.hide();
      this.flagAssess = {}
      this.currentAssess = {
          teacher_id: null,
          criteria_ids: [],
          groups: [],
          subject_id: null,
          unit_id: null,
          period_id: null,
        };
    },
    showSumWorkModalAdd() {
      this.modalTitle = 'Создание итоговой работы';
      this.formEditMode = false;
      this.currentAssess.teacher_id = this.authUser.teacher.id;
      this.currentAssess.period_id = this.currentPeriod.id;
      this.modalAssess.show();
      this.flagAssess.add = true;
    },
    showSumWorkModalEdit(id) {
      this.modalTitle = 'Редактирование итоговой работы';
      this.formEditMode = true;
      this.currentAssess = { ...this.sumWorks.find(item => item.id == id) };
      this.currentAssess.teacher_id = this.currentAssess.teacher.id;
      this.currentAssess.subject_id = this.currentAssess.subject.id;
      this.currentAssess.unit_id = this.currentAssess.unit.id;
      this.currentAssess.period_id = this.currentAssess.period;
      this.currentAssess.criteria_ids = this.currentAssess.criteria.map(item => item.id);
      this.currentAssess.groups = this.currentAssess.groups.map(item => {
        return {
          id: item.id,
          group_id: item.group.id,
          date: item.date,
          lesson: item.lesson,
        }
      })
      this.modalAssess.show();
      this.flagAssess.edit = true;
      
    },
    showSumWorkModalDelete(id) {
      this.modalTitle = 'Удаление итоговой работы';
      this.currentAssess = { ...this.sumWorks.find(item => item.id == id) };
      this.modalAssess.show();
      this.flagAssess.delete = true;
    },
    // Получение результатов валидации из компонента с формой
    validFormResult(value) {
      this.validForm = value;
    },
    sumWorkCreate() {
      this.$refs.assessmentForm.checkFieldsValidate();
      this.validForm = true
      if (this.validForm) {
        console.log("Запрос на создание итоговой работы: ", this.currentAssess);
        this.axios.post('assessment/sumwork', this.currentAssess).then((response) => {
        }).finally(() => {
          this.currentAssess = {};
          this.getSumWorkData({period: this.currentPeriod.id, teacher: this.authUser.teacher.id});
          this.hideSumWorkModal();
        });
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkEdit() {
      this.$refs.assessmentForm.checkFieldsValidate();
      if (this.validForm) {
        console.log("Запрос на изменение итоговой работы: ", this.currentAssess);
        this.axios.put(`assessment/sumwork/${this.currentAssess.id}`, this.currentAssess).then((response) => {
          }).finally(() => {
            this.currentAssess = {};
            this.getSumWorkData({period: this.currentPeriod.id, teacher: this.authUser.teacher.id});
            this.hideSumWorkModal();
          });
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkDelete() {
      console.log("Запрос на удаление итоговой работы");
      this.axios.delete(`assessment/sumwork/${this.currentAssess.id}`).then((response) => {
        }).finally(() => {
          this.currentAssess = {};
          this.getSumWorkData({period: this.currentPeriod.id, teacher: this.authUser.teacher.id});
          this.hideSumWorkModal();
        });
    },
    // преобраование массива итоговых работ в группированный по предмету объект массивов
    groupedSumWorks(array, fields) {
      let groupedObject = array.reduce((acc, obj) => {
        let objField = obj
        for (const field of fields) {
          objField = objField[field];
        }
        const property = objField.id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
    // Нахождение предмета по его ID
    getSubject(id) {
      return this.subjects.find(item => item.id == id); 
    },
    // Нахождение года обучения по его ID
    getGrade(id) {
      return this.grades.find(item => item.id == id); 
    },
    // Обновление итоговых работ при выборе периода
    refreshSumWorkBySubject(pr) {
      this.currentPeriod = pr;
      this.getSumWorkData({period: pr.id, teacher: this.authUser.teacher.id});
    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalAssess = new Modal('#modalAssess', { backdrop: 'static' });
    this.getTeachersData();
    this.getStudyYearsData();
    this.getSubjectsData('ooo', 'base');
    this.getGradesData();
    this.getPeriodsData(this.currentStudyYear).finally(() => {
      this.getSumWorkData({period: this.currentPeriod.id, teacher: this.authUser.teacher.id});
    });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser']),
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
  font-size: 2em;
  padding-bottom: 5px;
  border-bottom: 1px solid #ffbf40;
}
.sumworks-subject .title {
  font-weight: 700;
  text-transform: uppercase;
}
.sumworks-year {
  display: flex;
  align-items: center;
  background-color: #33cccc;
  padding: 10px;
}
.sumworks-year .title{
  color: #fff;
  font-weight: 700;
  font-size: 1.5rem;
}
.sumworks-year .sumassess {
  margin-left: auto;
  padding: 10px;
  background-color: #ffbf40;
  color: #000000;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 700;
}
.sumworks-year .sumassess:hover {
  background-color: #fad385;
}
.sumworks-grouped {
  border: 1px solid #33cccc;
  margin: 10px 0;
  padding: 10px;
}
</style>