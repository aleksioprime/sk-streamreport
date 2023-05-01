<template>
  <div>
    <base-header>
      <template v-slot:header>Мои юниты MYP</template>
    </base-header>
    <div class="col-md-3 d-flex">
      <button type="button" class="btn btn-primary mb-2" @click="showAddUnit">
        Cоздать юнит
      </button>
    </div>
    <!-- Инструменты фильтрации юнитов -->
    <unit-filter :years="years" @updateFetch="updateFetchUnitMYP" :subjects="subjects"/>
    <!-- Список юнитов -->
    <div v-if="!isUnitLoading" class="mt-3">
      <unit-myp-list :units="unitsMYP" @changePage="changePage" :totalPages="totalPages" :currentPage="currentPage" />
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <!-- Модальное окно с формой добавления юнита -->
    <modal-unit :modalTitle="modalTitle" :flagUnit="flagUnit" @cancel="hideUnitModal" @create="unitCreate">
      <unit-myp-form v-if="flagUnit.add" ref="formUnit" v-model:editedUnit="editedUnit" v-model:validFormUnit="validFormUnit"/>
      <div v-if="flagUnit.delete">
          <div>Вы действительно хотите удалить этот юнит?</div>
          <div>
            <div>{{ editedUnit.title }}</div>
          </div>
        </div>
    </modal-unit>
  </div>
</template>
  
<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex'
import UnitMypList from "@/components/unit/myp/UnitMYPList";
import UnitFilter from "@/components/unit/myp/UnitFilter";
import UnitMypForm from "@/components/unit/myp/UnitMYPForm";

import { getUnitsMYP, createUnitMYP } from "@/hooks/unit/useUnitMYP";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getSubjects } from "@/hooks/curriculum/useSubject";

export default {
  name: 'UnitMYP',
  components: {
    UnitMypList, UnitFilter, UnitMypForm
  },
  setup(props) {
    const { unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP } = getUnitsMYP();
    const { createdUnitMYP, fetchCreateUnitMYP } = createUnitMYP();
    const { years, fetchGetClassYears } = getClassYears();
    const { subjects, fetchGetSubjects } = getSubjects();
    return {
      unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP,
      createdUnitMYP, fetchCreateUnitMYP,
      years, fetchGetClassYears,
      subjects, fetchGetSubjects,
    }
  },
  data() {
    return {
      currentPage: 1,
      limit: 15,
      flagUnit: {},
      validFormUnit: false,
      editedUnit: {},
      modalTitle: null,
      queryYears: [],
      adminMode: false,
    }
  },
  methods: {
    // Выбор текущей страницы
    changePage(page) {
      this.currentPage = page;
      this.fetchGetUnitsMYP({ page: this.currentPage, limit: this.limit });
    },
    // Открытие модального окна для добавления юнита 
    showAddUnit() {
      this.modalTitle = "Добавление юнита MYP";
      this.flagUnit.add = true;
      this.editedUnit = {
        class_year_id: null,
        subject_id: null,
        authors_ids: [],
        criteria_ids: [],
      };
      this.modalUnit.show();
    },
    // Открытие модального окна для удаления юнита 
    showDelUnit(unit) {
      this.modalTitle = "Удаление юнита MYP";
      this.editedUnit = unit;
      this.flagUnit.delete = true;
      this.modalUnit.show();
    },
    // Закрытие модального окна
    hideUnitModal() {
      this.validFormUnit = false;
      this.editedUnit = {};
      this.modalUnit.hide();
      this.flagUnit = {};
    },
    // Создание юнита (отправка post запроса на сервер)
    unitCreate() {
      this.$refs.formUnit.checkFieldsValidate();
      if (this.validFormUnit) {
        console.log("Запрос на создание юнита: ", this.editedUnit);
        this.fetchCreateUnitMYP(this.editedUnit).then(() => {
          this.fetchGetUnitsMYP({ page: this.currentPage, limit: this.limit });
          this.hideUnitModal();
        })
      } else {
        console.log('Валидация неуспешна', this.editedUnit)
      }
    },
    //
    updateFetchUnitMYP(data) {
      console.log('Выбранные фильтры: ', data)
      if (this.adminMode) {
        this.fetchGetUnitsMYP({ years: data.years, subject: data.subject, page: this.currentPage, limit: this.limit });
      } else {
        this.fetchGetClassYears({ teacher: this.authUser.teacher.id, program: 'MYP', subject: data.subject });
        this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, years: data.years, subject: data.subject, page: this.currentPage, limit: this.limit });
      }
      
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    // Определение модального окна для создания юнита
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, page: this.currentPage, limit: this.limit });
    this.fetchGetClassYears({ teacher: this.authUser.teacher.id, program: 'MYP' });
    this.fetchGetSubjects({ teacher: this.authUser.teacher.id, level: 'ooo', type: 'base' });    
  },
}
</script>
  
<style scoped></style>