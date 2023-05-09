<template>
  <div class="block-filter">
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear" @change="resetQuery">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
            {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <!-- Выбор периодов обучения -->
    <div class="block-period">
      <div v-for="pr in reportPeriods" :key="pr.id" class="period">
        <input type="radio" name="period" :value="pr" :id="'period-' + pr.id"
          v-model="currentReportPeriod" @change="handleQuery">
        <label :for="'period-' + pr.id">
        <div class="period-title">{{ pr.number }} период</div>
        <div class="period-item-date">{{ new Date(pr.date_start).toLocaleDateString() }} - {{ new Date(pr.date_end).toLocaleDateString() }}</div>
        </label>
      </div>
    </div>
    
    <div class="row">
      <!-- Выбор года обучения -->
      <div class="col-md">
        <select id="class-year" class="form-select me-3 mb-2" v-model="currentClassYear" @change="getClassGroups">
          <option :value="null">Выберите год</option>
          <option v-for="(year, i) in years" :key="i" :value="year.id">
              {{ year.year_rus }} классы
          </option>
        </select>
      </div>
      <!-- Выбор класса -->
      <div class="col-md">
        <select id="class-group" class="form-select me-3 mb-2" v-model="currentGroup" @change="handleQuery" :disabled="!groups.length">
          <option :value="null">Выберите класс</option>
          <option v-for="(gr, i) in groups" :key="i" :value="gr.id">
              {{ gr.class_year }}{{ gr.letter }} класс
          </option>
        </select>
      </div>
    </div>
    <!-- Выбор предмета -->
    <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubject" @change="handleQuery">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getTeachers } from "@/hooks/user/useUser";
import { getGroups } from "@/hooks/user/useGroup";

export default {
  props: {
    
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { years, fetchGetClassYears } = getClassYears();
    const { groups, fetchGetGroups } = getGroups();
    const { teachers, isTeacherLoading, fetchGetTeachers } = getTeachers();
    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
      subjects, fetchGetSubjects,
      years, fetchGetClassYears,
      groups, fetchGetGroups,
      teachers, isTeacherLoading, fetchGetTeachers
    }
  },
  data() {
    return {
      currentClassYear: null,
      currentGroup: null,
      currentSubject: null,
    }
  },
  methods: {
    resetQuery() {
      this.currentClassYear = null;
      this.currentSubject = null;
      this.currentGroup = null;
    },
    getClassGroups() {
      this.currentGroup = null;
      this.handleQuery();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, class_year: this.currentClassYear});
    },
    handleQuery(event) {
      this.$emit('updateFetch', { 
        study_year: this.currentStudyYear.id,
        class_year: this.currentClassYear, 
        period: this.currentReportPeriod,
        subject: this.currentSubject,
        group: this.currentGroup,
      });
    },
    handleStudyYear() {
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear })
    }
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear })
    });
    this.fetchGetClassYears({ program: 'MYP' });
    this.fetchGetSubjects({ level: 'ooo', type: 'base' });
  },
  watch: {
    
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
  margin-top: 5px;
}

</style>