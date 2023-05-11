<template>
  <div>
    <base-header>
      <template v-slot:header>Мои итоговые работы</template>
    </base-header>
    <button type="button" class="btn btn-primary" @click="showSumWorkModalAdd">
      Cоздать итоговую работу
    </button>
    <assessment-filter @updateFetch="updateFetch" :studyPrograms="studyPrograms"/>
    <!-- Модальное окно добавления/редактирования/удаления итоговой работы -->
    <modal-assess :modalTitle="modalTitle" :flagAssess="flagAssess" 
      @create="sumWorkCreate" @delete="sumWorkDelete" @update="sumWorkEdit" @cancel="hideSumWorkModal">
      <template v-slot:body>
        <!-- Форма добавления/редактирования итоговой работы -->
        <assessment-form v-model:summativeWork="currentAssess" v-if="flagAssess.add || flagAssess.edit"
        :studyPrograms="studyPrograms" @validForm="validFormResult" ref="assessmentForm" :editMode="formEditMode"/>
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
    
    <!-- Вывод итоговых работ учителя, сгруппированных по предметам -->
    <div v-if="Object.keys(groupedSumWorks(summativeWorks, ['subject'])).length !== 0" class="sumworks">
      <div v-for="(worksBySubject, subject) in groupedSumWorks(summativeWorks, ['subject'])" :key="subject">
        <div class="sumworks-subject" v-if="getSubject(subject)">{{ getSubject(subject).name_rus }}</div>
        <div v-for="(worksByYear, year) in groupedSumWorks(worksBySubject, ['unit', 'class_year'])" :key="year" class="sumworks-block">
          <div class="sumworks-year">
            <div class="title" v-if="getGrade(year)">{{ getGrade(year).year_rus }} {{  }} классы</div>
          </div>
          <div class="sumworks-grouped">
            <assessment-item v-for="sumwork in worksByYear" :key="sumwork.id" :sumwork="sumwork" @editWork="showSumWorkModalEdit(sumwork.id)" @deleteWork="showSumWorkModalDelete(sumwork.id)"/>
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
import AssessmentForm from "@/components/assessment/AssessmentForm.vue";
import AssessmentItem from "@/components/assessment/AssessmentItem.vue";
import AssessmentFilter from "@/components/assessment/AssessmentFilter.vue";
import { getSummativeWorks, createSummativeWork, updateSummativeWork, deleteSummativeWork } from "@/hooks/assess/useSummativeWork";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'Assessment',
  components: {
    AssessmentForm, AssessmentItem, AssessmentFilter
  },
  setup(props) {
    const { summativeWorks, isSumWorkLoading, fetchGetSummativeWorks } = getSummativeWorks();
    const { createdSummativeWork, fetchCreateSummativeWork } = createSummativeWork();
    const { updatedSummativeWork, fetchUpdateSummativeWork } = updateSummativeWork();
    const { fetchDeleteSummativeWork } = deleteSummativeWork();
    const { groupedArrayData } = getGroupedArray();

    return {
      summativeWorks, isSumWorkLoading, fetchGetSummativeWorks,
      createdSummativeWork, fetchCreateSummativeWork,
      updatedSummativeWork, fetchUpdateSummativeWork,
      fetchDeleteSummativeWork,
      groupedArrayData
    }
  },
  data() {
    return {
      currentPeriod: null,
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
      studyPrograms: [
        { value: 'PYP', name_eng: 'Primary Years Programme', name_rus: 'Программа начальной школы' },
        { value: 'MYP', name_eng: 'Middle Years Programme', name_rus: 'Программа средней школы' },
        { value: 'DP', name_eng: 'Diploma Programme', name_rus: 'Программа старшей школы DP' },
        { value: 'FGOS', name_eng: 'ФГОС', name_rus: 'Программа старшей школы ФГОС' },
      ]
    }
  },
  methods: {
    updateFetch(data) {
      this.currentPeriod = data.period;
      console.log('Параметры фильтрации: ', data)
      this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
    },
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
      this.currentAssess = { ...this.summativeWorks.find(item => item.id == id) };
      this.currentAssess.teacher_id = this.currentAssess.teacher.id;
      this.currentAssess.subject_id = this.currentAssess.subject.id;
      this.currentAssess.unit_id = this.currentAssess.unit.id;
      this.currentAssess.period_id = this.currentAssess.period.id;
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
      this.currentAssess = { ...this.summativeWorks.find(item => item.id == id) };
      this.modalAssess.show();
      this.flagAssess.delete = true;
    },
    // Получение результатов валидации из компонента с формой
    validFormResult(value) {
      this.validForm = value;
    },
    sumWorkCreate() {
      this.$refs.assessmentForm.checkFieldsValidate();
      if (this.validForm) {
        console.log("Запрос на создание итоговой работы: ", this.currentAssess);
        this.fetchCreateSummativeWork(this.currentAssess).finally(() => {
          this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
          this.hideSumWorkModal();
          this.currentAssess = {};
        })
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkEdit() {
      this.$refs.assessmentForm.checkFieldsValidate();
      if (this.validForm) {
        console.log("Запрос на изменение итоговой работы: ", this.currentAssess);
        this.fetchUpdateSummativeWork(this.currentAssess.id, this.currentAssess).finally(() => {
          this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
          this.hideSumWorkModal();
          this.currentAssess = {};
        });
      } else {
        console.log('Валидация неуспешна', this.currentAssess)
      }
    },
    sumWorkDelete() {
      console.log("Запрос на удаление итоговой работы");
      this.fetchDeleteSummativeWork(this.currentAssess.id).finally(() => {
        this.fetchGetSummativeWorks({period: this.currentPeriod.id, teacher: this.authUser.teacher.id})
        this.hideSumWorkModal();
        this.currentAssess = {};
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
    // Нахождение предмета по его ID из списка итоговых работ
    getSubject(id) {
      let subject = null;
      this.summativeWorks.forEach((item) => {
        if (item.subject.id == id) {
          subject = item.subject
          return
        }
      })
      return subject
    },
    // Нахождение года обучения по его ID из списка итоговых работ
    getGrade(id) {
      let year = null;
      this.summativeWorks.forEach((item) => {
        if (item.unit.class_year.id == id) {
          year = item.unit.class_year
          return
        }
      })
      return year
    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalAssess = new Modal('#modalAssess', { backdrop: 'static' });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>

<style>
.tools {
  display: flex;
  align-items: center;
}
.tools .btn {
  max-width: 300px;
}
.sumworks {
  display: flex;
  flex-direction: column;
  padding: 10px;
}
.sumworks-block {
  border: 2px solid #c4c4c4;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
  border-radius: 5px;
  margin-top: 10px;
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
  background-color: #c4c4c4;
  padding: 10px;
  cursor: pointer;
}
.sumworks-year:hover {
  transition: 0.6s;
  background-color: #a3a3a3;
}
.sumworks-block:hover {
  transition: 1s;
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.5);
}
.sumworks-year .title{
  color: #fff;
  font-weight: 700;
  font-size: 1.5rem;
}
.sumworks-year .sumassess {
  margin-left: auto;
  padding: 10px;
  color: #000000;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 700;
}
.sumworks-year .sumassess:hover {
  background-color: #fad385;
}
.sumworks-grouped {
  padding: 10px;
}

</style>