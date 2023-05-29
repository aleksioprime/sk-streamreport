<template>
  <div>
    <base-header>
      <template v-slot:header>Учебный план</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <div class="program-wrapper">
      <div class="radiobutton" v-for="plan in academicPlans" :key="plan.id">
        <input type="radio" name="program" :value="plan" :id="`program-${plan.id}`" @change="changeProgram"
          v-model="currentPlan">
        <label :for="`program-${plan.id}`">
          <div>{{ plan.name_rus }}</div>
        </label>
      </div>
    </div>
    <div class="wrapper-title"><h2>Обязательная часть</h2></div>
    <div class="subject-wrapper" v-if="baseSubjects.length">
      <syllabus-item v-for="(dataSubjects, subject) in groupedArrayData(baseSubjects, ['subject', 'id'])" :key="subject" 
      :subject="getSubjectByAcademicPlan(subject)" :dataSubjects="dataSubjects" @deleteItem="showHoursDelete" v-model:editableItem="editableItem">
        <template v-slot:form>
          <button class="icon icon-add mt-2" @click="showHoursAdd(subject)" v-show="editableSubject != subject"></button>
          <syllabus-form v-if="editableSubject == subject" :years="years" :subjects="subjects" 
            :editableData="editableData" :deletionMode="deletionMode"
            @apply="applyEditHours" @cancel="cancelEditHours"/>
        </template>
      </syllabus-item>
    </div>
    <div class="subject-wrapper area" v-else>Нет данных</div>
    <button v-show="currentPlan.id && !addSubjectBase" class="btn btn-primary" @click="showSubjectAdd(type='base')">Добавить предмет c нагрузкой</button>
    <syllabus-form v-if="addSubjectBase" :years="years" :subjects="filteredSubjects" 
          :editableData="editableData" :deletionMode="deletionMode"
          @apply="applyEditHours" @cancel="cancelEditHours"/>
    <div class="wrapper-title"><h2>Внеурочная деятельность</h2></div>
    <div class="subject-wrapper" v-if="extraSubjects.length">
      <syllabus-item v-for="(dataSubjects, subject) in groupedArrayData(extraSubjects, ['subject', 'id'])" :key="subject" v-model:editableItem="editableItem"
      :subject="getSubjectByAcademicPlan(subject)" :dataSubjects="dataSubjects" @deleteItem="showHoursDelete">
        <template v-slot:form>
          <button class="icon icon-add mt-2" @click="showHoursAdd(subject)" v-show="editableSubject != subject"></button>
          <syllabus-form v-if="editableSubject == subject" :years="years" :subjects="subjects" 
            :editableData="editableData" :deletionMode="deletionMode"
            @apply="applyEditHours" @cancel="cancelEditHours"/>
        </template>
      </syllabus-item>
      <!-- <div v-for="(dataSubjects, subject) in groupedArrayData(extraSubjects, ['subject', 'id'])" :key="subject"
        class="plan-item area">
        <div class="subject-title">
          <h3>{{ getSubjectByAcademicPlan(subject).name_rus }}</h3>
          <div v-if="getSubjectByAcademicPlan(subject).group_fgos">{{ getSubjectByAcademicPlan(subject).group_fgos.type }}: {{
            getSubjectByAcademicPlan(subject).group_fgos.name_rus }}</div>
        </div>
        <div class="subject-hours">
          <div v-for="sb in dataSubjects" :key="sb.id" class="subject-hours-item popup" :class="{ 'editable-item':  editableData.id == sb.id }" @click="showEditButton(sb.id)">
            <div><span v-for="year, index in sb.years" :key="year.id">{{ year.year_rus }}<span v-if="++index !== sb.years.length">,&nbsp;</span></span> класс:</div>
            <div>{{ getWordHour(sb.hours) }}</div>
            <div :id="`popup-icon-${sb.id}`" class="popuptext">
              <button class="icon icon-edit" @click="showHoursEdit(sb)"></button>
              <button class="icon icon-del" @click="showHoursDelete(sb)"></button>
            </div>
          </div>
        </div>
        <button class="icon icon-add mt-2" @click="showHoursAdd(subject)" v-show="editableSubject != subject"></button>
        <syllabus-form v-if="editableSubject == subject" :years="years" :subjects="subjects" 
          :editableData="editableData" :deletionMode="deletionMode"
          @apply="applyEditHours" @cancel="cancelEditHours"/>
      </div> -->
    </div>
    <div class="subject-wrapper area" v-else>Нет данных</div>
    <button v-show="currentPlan.id && !addSubjectExtra" class="btn btn-primary" @click="showSubjectAdd(type='extra')">Добавить предмет с нагрузкой</button>
    <syllabus-form v-if="addSubjectExtra" :years="years" :subjects="filteredSubjects" 
          :editableData="editableData" :deletionMode="deletionMode"
          @apply="applyEditHours" @cancel="cancelEditHours"/>
  </div>
</template>

<script>
import SyllabusForm from "@/components/curriculum/SyllabusForm";
import SyllabusItem from "@/components/curriculum/SyllabusItem.vue";

import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getAcademicPlan, getAcademicPlans, createHoursSubject, updateHoursSubject, deleteHoursSubject } from "@/hooks/curriculum/useAcademicPlan";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getSubjects } from "@/hooks/curriculum/useSubject";

export default {
  name: 'AdminSyllabus',
  components: {
    SyllabusForm, SyllabusItem
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { academicPlans, fetchGetAcademicPlans } = getAcademicPlans();
    const { academicPlan, fetchGetAcademicPlan } = getAcademicPlan();
    const { createdHoursSubject, fetchCreateHoursSubject } = createHoursSubject();
    const { updatedHoursSubject, fetchUpdateHoursSubject } = updateHoursSubject();
    const { fetchDeleteHoursSubject } = deleteHoursSubject();
    const { groupedArrayData } = getGroupedArray();
    const { years, fetchGetClassYears } = getClassYears();
    const { subjects, fetchGetSubjects } = getSubjects();

    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      academicPlan, fetchGetAcademicPlan,
      academicPlans, fetchGetAcademicPlans,
      createdHoursSubject, fetchCreateHoursSubject,
      updatedHoursSubject, fetchUpdateHoursSubject,
      fetchDeleteHoursSubject,
      groupedArrayData,
      years, fetchGetClassYears,
      subjects, fetchGetSubjects
    }
  },
  data() {
    return {
      currentPlan: {
        subject_year: []
      },
      editableSubject: null,
      editableData: {},
      deletionMode: false,
      addSubjectBase: false,
      addSubjectExtra: false,
      editableItem: null,
    }
  },
  methods: {
    showSubjectAdd(type = null) {
      this.cancelEditHours();
      this.fetchGetClassYears({ level: this.currentPlan.level });
      this.fetchGetSubjects({ level: this.currentPlan.level, type: type });
      if (type == 'base') {
        this.addSubjectBase = true;
      } else if (type == 'extra') {
        this.addSubjectExtra = true;
      }
      this.editableData = { years_ids: [], subject_id: null }
    },
    showHoursAdd(id = null) {
      this.cancelEditHours();
      this.subjects = [ this.getSubjectByAcademicPlan(id) ]
      this.fetchGetClassYears({ level: this.currentPlan.level });
      this.editableSubject = id;
      this.editableData = { years_ids: [], subject_id: id }
    },
    showHoursEdit(data) {
      this.years = [ data.years ]
      this.subjects = [ data.subject ]
      this.editableSubject = data.subject.id;
      this.editableData = { id: data.id, years_ids: data.years.map(item => item.id), subject_id: data.subject.id, hours: data.hours }
    },
    showHoursDelete(data) {
      console.log(data)
      this.deletionMode = true;
      this.editableSubject = data.subject.id;
      this.editableData = { id: data.id }
    },
    applyEditHours(data) {
      if (this.deletionMode) {
        console.log('Удаление нагрузки: ', data.id)
        this.fetchDeleteHoursSubject(data.id).finally(() => {
          this.fetchGetAcademicPlan(this.currentPlan.id).finally(() => {
            this.currentPlan = this.academicPlan;
          })
        })
      } else if (data.id) {
        data.academic_plan_id = this.currentPlan.id
        console.log('Редактирование нагрузки: ', data)
        // this.fetchUpdateHoursSubject(data.id, data).finally(() => {
        //   this.fetchGetAcademicPlan(this.currentPlan.id).finally(() => {
        //     this.currentPlan = this.academicPlan;
        //   })
        // })
      } else {
        data.academic_plan_id = this.currentPlan.id
        console.log('Добавление нагрузки: ', data)
        this.fetchCreateHoursSubject(data).finally(() => {
          this.fetchGetAcademicPlan(this.currentPlan.id).finally(() => {
            const index = this.academicPlans.findIndex(item => item.id == data.academic_plan_id);
            if (index != -1) {
              this.academicPlans[index] = this.academicPlan
              this.currentPlan = this.academicPlans[index]
            }

          })
        })
      }
      this.cancelEditHours();
    },
    cancelEditHours() {
      this.editableSubject = null;
      this.deletionMode = false;
      this.editableData = {}
      this.addSubjectBase = false;
      this.addSubjectExtra = false;
      this.editableItem = null;
    },
    // showEditButton(id) {
    //   document.querySelectorAll(`.popuptext`).forEach((item) => {
    //     if (item.classList.contains('show')) {
    //       item.classList.remove('show')
    //     }
    //   })
    //   if (!this.editSubjectMode) {
    //     const popup = document.querySelector(`#popup-icon-${id}`);
    //     popup.classList.toggle('show')
    //   } 
    // },
    getWordHour(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} часов`;
      if (number > 1 && number < 5) return `${count} часа`;
      if (number == 1) return `${count} час`;
      return `${count} часов`;
    },
    getSubjectByAcademicPlan(id) {
      const data = this.currentPlan.subject_year.find(item => item.subject.id == id)
      if (data) {
        return data.subject
      }
      return {}
    }
  },
  computed: {
    baseSubjects() {
      return this.currentPlan.subject_year.filter(item => item.subject.type == 'base')
    },
    extraSubjects() {
      return this.currentPlan.subject_year.filter(item => item.subject.type == 'extra')
    },
    filteredSubjects() {
      return this.subjects.filter(item => !this.currentPlan.subject_year.map(obj => obj.subject.id).includes(item.id))
    }
  },
  mounted() {
    // document.addEventListener('click', function (event) {
    //   if (!this.editSubjectMode) {
    //     if (!event.target.classList.contains('popup') && !event.target.parentNode.classList.contains('popup')) {
    //       document.querySelectorAll(`.popuptext`).forEach((item) => {
    //         if (item.classList.contains('show')) {
    //           item.classList.remove('show')
    //         }
    //       })
    //     }
    //   }
    // })
    this.fetchGetStudyYears().finally(() => {
      this.fetchGetAcademicPlans({ study_year: this.currentStudyYear.id }).finally(() => {
        this.currentPlan = this.academicPlans[0];
      })
    })
  }
}
</script>

<style scoped>
.program-wrapper {
  display: flex;
  gap: 5px;
}
.wrapper-title {
  text-transform: uppercase;
  margin-top: 20px;
}
.plan-item {}

/* Popup container */
.popup {
  position: relative;
  cursor: pointer;
}

/* The actual popup (appears on top) */
.popup .popuptext {
  visibility: hidden;
  background-color: var(--my-focus);
  color: #000;
  text-align: center;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  top: -100%;
  right: 0;
  width: 80px;
}

/* Popup arrow */
.popup .popuptext::after {
  content: "";
  position: absolute;
  top: 100%;
  /* left: 50%; */
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: var(--my-focus) transparent transparent transparent;
}

/* Toggle this class when clicking on the popup container (hide and show the popup) */
.popup .show {
  visibility: visible;
  -webkit-animation: fadeIn 0.5s;
  animation: fadeIn 0.5s
}

/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>