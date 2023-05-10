<template>
  <div>
    <base-header>
      <template v-slot:header>
        <div>MYP: список <span v-if="showAllUnits">всех</span><span v-else>моих</span> юнитов</div>
        
      </template>
    </base-header>
    <div class="row">
      <div class="col-md mb-2">
        <button type="button" class="btn btn-primary btn-create" @click="showAddUnit">
          Cоздать юнит
        </button>
        <button type="button" class="btn btn-primary btn-create" @click="showAddIDU">
          Cоздать МДП
        </button>
      </div>
      <div class="col-md-3 mb-2 d-flex show-toggle" v-if="isAdmin">
        <div class="show-toggle-item my ms-auto">
          <input id="show-my" type="radio" :value="false" v-model="showAllUnits">
          <label for="show-my">Мои</label>
        </div>
        <div class="show-toggle-item all">
          <input id="show-all" type="radio" :value="true" v-model="showAllUnits">
          <label for="show-all">Все</label>
        </div>
      </div>
    </div>
    <!-- Инструменты фильтрации юнитов -->
    <unit-filter :showAllUnits="showAllUnits" :user="authUser" @updateFetch="getFilters"/>
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
    <modal-unit :modalId="'modalUnit'" :modalTitle="modalTitle" :flagUnit="flagUnit" @cancel="hideUnitModal" @create="unitCreate">
      <unit-myp-form v-if="flagUnit.add" ref="formUnit" v-model:editedUnit="editedUnit" v-model:validFormUnit="validFormUnit"/>
      <div v-if="flagUnit.delete">
        <div>Вы действительно хотите удалить этот юнит?</div>
        <div>
          <div>{{ editedUnit.title }}</div>
        </div>
      </div>
    </modal-unit>
    <!-- Модальное окно с формой добавления МДП -->
    <modal-unit :modalId="'modalUnitIDU'" :modalTitle="modalTitle" :flagUnit="flagUnitIDU" @cancel="hideUnitIDUModal" @create="unitIDUCreate">
      <unit-myp-idu-form v-if="flagUnitIDU.add" ref="formUnitIDU" v-model:editedUnit="editedUnitIDU" v-model:validFormUnit="validFormUnitIDU"/>
    </modal-unit>
  </div>
</template>
  
<script>
import { Modal } from 'bootstrap';
import { mapGetters } from 'vuex';
import UnitMypList from "@/components/unit/myp/UnitMYPList";
import UnitFilter from "@/components/unit/myp/UnitFilter";
import UnitMypForm from "@/components/unit/myp/UnitMYPForm";
import UnitMypIduForm from "@/components/unit/myp/UnitMYPIDUForm";

import { getUnitsMYP, createUnitMYP } from "@/hooks/unit/useUnitMYP";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { createInterdisciplinaryUnit } from "@/hooks/unit/useInterdisciplinaryUnit";

export default {
  name: 'UnitMYP',
  components: {
    UnitMypList, UnitFilter, UnitMypForm, UnitMypIduForm
  },
  setup(props) {
    const { unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP } = getUnitsMYP();
    const { createdUnitMYP, fetchCreateUnitMYP } = createUnitMYP();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { interdisciplinaryUnit, fetchCreateInterdisciplinaryUnit } = createInterdisciplinaryUnit();
    return {
      unitsMYP, isUnitLoading, totalPages, totalUnits, fetchGetUnitsMYP,
      createdUnitMYP, fetchCreateUnitMYP,
      subjects, fetchGetSubjects,
      interdisciplinaryUnit, fetchCreateInterdisciplinaryUnit,
    }
  },
  data() {
    return {
      currentPage: 1,
      limit: 15,
      flagUnit: {},
      flagUnitIDU: {},
      validFormUnit: false,
      validFormUnitIDU: false,
      editedUnit: {},
      editedUnitIDU: {},
      modalTitle: null,
      showAllUnits: false,
      currentFilter: {
        department: null,
        subject: null,
        years: []
      }
    }
  },
  methods: {
    // Выбор текущей страницы
    changePage(page) {
      this.currentPage = page;
      this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, page: this.currentPage, limit: this.limit });
    },
    // Открытие модального окна для добавления юнита 
    showAddUnit() {
      this.modalTitle = "Создание юнита MYP";
      this.flagUnit.add = true;
      this.editedUnit = {
        class_year_id: null,
        subject_id: null,
        level_id: null,
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
          this.updateFetchUnitMYP();
          this.hideUnitModal();
        })
      } else {
        console.log('Валидация неуспешна', this.editedUnit)
      }
    },
    getFilters(data) {
      console.log('Выбранные фильтры: ', data)
      this.currentFilter.department = data.department;
      this.currentFilter.subject = data.subject;
      this.currentFilter.years = data.years;
      this.updateFetchUnitMYP();
    },
    //
    updateFetchUnitMYP() {
      if (this.showAllUnits) {
        this.fetchGetUnitsMYP({ department: this.currentFilter.department, years: this.currentFilter.years, subject: this.currentFilter.subject, limit: this.limit });   
      } else {
        this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, years: this.currentFilter.years, subject: this.currentFilter.subject, limit: this.limit });
      }
    },
    showAddIDU() {
      this.modalTitle = "Создание междисциплинарного юнита MYP";
      this.editedUnitIDU = {
        class_year_id: null,
        criteria_ids: [],
        unitplan_myp_ids: [],
      };
      this.flagUnitIDU.add = true;
      this.modalUnitIDU.show();
    },
    hideUnitIDUModal() {
      this.modalUnitIDU.hide();
    },
    unitIDUCreate() {
      this.$refs.formUnitIDU.checkFieldsValidate();
      if (this.validFormUnitIDU) {
        console.log("Запрос на создание юнита: ", this.editedUnitIDU);
        this.fetchCreateInterdisciplinaryUnit(this.editedUnitIDU).finally(() => {
          this.fetchGetUnitsMYP({ teacher: this.authUser.teacher.id, page: this.currentPage, limit: this.limit });
          this.hideUnitIDUModal();
        })
      } else {
        console.log('Валидация неуспешна', this.editedUnitIDU)
      }
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  watch: {
    showAllUnits() {

    }
  },
  mounted() {
    // Определение модального окна для создания юнита
    this.modalUnit = new Modal('#modalUnit', { backdrop: 'static' });
    this.modalUnitIDU = new Modal('#modalUnitIDU', { backdrop: 'static' });
    if (this.isAdmin) {
      this.showAllUnits = true;
    } else {
      this.updateFetchUnitMYP();
    }
  },
}
</script>
  
<style scoped>
@import '@/assets/css/spinner.css';
.loader {
  display: flex;
  height: calc(100vh - 200px);
  align-items: center;
  justify-content: center;
}
.btn-create {
  min-width: 160px;
}
.btn-create:not(:nth-of-type(-1)) {
  margin-right: 10px;
}
.show-toggle {
	display: inline-block;
	overflow: hidden;
}
.show-toggle-item {
	float: left;
	display: inline-block;
}
.show-toggle-item input[type=radio] {
	display: none;
}
.show-toggle-item label {
	display: inline-block;
	padding: 0px 15px;   
	line-height: 34px;    
	border: 1px solid #999;
	border-right: none;
	cursor: pointer;
	user-select: none;   
}
 
.show-toggle .my label {
	border-radius: 6px 0 0 6px;
}
.show-toggle .all label {
	border-radius: 0 6px 6px 0;
	border-right: 1px solid #999;
}
 
/* Checked */
.show-toggle .my input[type=radio]:checked + label {
	background: #ffc5c5;
}
.show-toggle .all input[type=radio]:checked + label {
	background: #bbffbb;
}
</style>