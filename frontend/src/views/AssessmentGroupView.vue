<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговое оценивание</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="row">
      <div class="col-md my-2">
        <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
          <option v-for="(study, i) in studyYears" :key="i" :value="study">
            {{ study.name }} учебный год
          </option>
        </select>
      </div>
      <!-- Выбор программы -->
      <div class="col-md my-2">
        <select id="programs" class="form-select me-3 mb-2" v-model="currentProgram">
          <option v-for="(pr, i) in programs" :key="i" :value="pr.value">
            {{ pr.name }}
          </option>
        </select>
      </div>
    </div>
    <!-- Выбор предмета -->
    <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubject">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div>


    <div v-if="!isGroupLoading">
      <div v-for="(groupsByYear, year) in groupedArrayData(groups, ['class_year'])" :key="year">
        <div class="class-group">{{ year }} классы</div>
        <div v-for="group in groupsByYear" :key="group.id" class="class-item">
          <div>{{ group.class_year }}{{ group.letter }} класс ({{ getWordStudent(group.count) }})</div>
          <div class="class-wrapper" v-if="currentSubject">
            <div class="assessment-title">Итоговые оценки по предмету {{ currentSubject.name_rus }}</div>
            <div class="assessment-period">
              <div class="period-item" v-for="period in periodClass(year)" :key="period.id">
                <div class="period-title">{{ period.number }} {{ period.type }}</div>
                <div class="period-info"></div>
                <button class="period-btn" v-if="currentSubject" @click="$router.push(`/assessment/group/${group.id}/period/${period.id}/subject/${currentSubject.id}`)">
                  Оценки
                </button>
              </div>
            </div>
            <div class="report-title">Репорты учителя ({{ authUser.teacher.last_name }} {{ authUser.teacher.first_name }} {{ authUser.teacher.middle_name }})</div>
            <div class="report-period">
              <div class="period-item" v-for="period in reportPeriods" :key="period.id">
                <div class="period-title">{{ period.name }}</div>
                <div class="period-info"></div>
                <button class="period-btn" v-if="currentSubject" @click="$router.push(`/report/teacher/group/${group.id}/subject/${currentSubject.id}/`)">
                  Репорты
                </button>
              </div>
              <button class="btn btn-primary" @click="$router.push(`/report/mentor/group/${group.id}/`)">Наставник</button>
              <button class="btn btn-primary" v-if="authUser && group.psychologist && authUser.teacher.id == group.psychologist.id">Психолог</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getGroups } from "@/hooks/user/useGroup";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";
import { getSubjects } from "@/hooks/curriculum/useSubject";
import { getPeriods } from "@/hooks/assess/usePeriod";
import { getReportPeriods } from "@/hooks/assess/useReportPeriod";
import { mapGetters } from 'vuex';

export default {
  components: {
    
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { groupedArrayData } = getGroupedArray();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { periods, fetchGetPeriods } = getPeriods();
    const { reportPeriods, currentReportPeriod, fetchGetReportPeriods } = getReportPeriods();

    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      groups, isGroupLoading, fetchGetGroups,
      groupedArrayData,
      subjects, fetchGetSubjects,
      periods, fetchGetPeriods,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods
    }
  },
  data() {
    return {
      currentSubject: null,
      currentProgram: 'MYP',
      programs: [
        { value: 'PYP', name: 'Программа начальной школы' },
        { value: 'MYP', name: 'Программа средней школы' },
        { value: 'DP', name: 'Программа старшей школы IB' },
        { value: 'FGOS', name: 'Программа старшей школы ФГОС' },
      ]
    }
  },
  methods: {
    getWordStudent(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} студентов`;
      if (number > 1 && number < 5) return `${count} студента`;
      if (number == 1) return `${count} студент`;
      return `${count} студентов`;
    },
    periodClass(classYear) {      
      return this.periods.filter(item => item.class_year.map(year => year.year_rus).includes(Number(classYear)))
    },
  },
 
  mounted() {
    this.fetchGetStudyYears();
    this.fetchGetGroups({ study_year: this.currentStudyYear, program: this.currentProgram }).finally(() => {
      this.fetchGetPeriods({ study_year: this.currentStudyYear })
      this.fetchGetReportPeriods({ study_year: this.currentStudyYear })
    });
    this.fetchGetSubjects({ level: 'ooo', type: 'base' });
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
}
</script>

<style>
@import '@/assets/css/spinner.css';
.class-group {
  text-transform: uppercase;
  font-size: 1.5em;
  margin-top: 10px;
}
.class-item {
  padding: 10px;
  border: 1px solid #a7a7a78a;
  border-radius: 5px;
  margin-top: 5px;
  display: flex;
  /* align-items: center; */
  flex-direction: column;
}
/* .class-item:hover {
 background: #a7a7a78a;
} */
.class-btns {
  margin-top: 10px;
  display: flex;
}
.class-btns .btn {
  margin-right: 5px;
}
.assessment-title, .report-title {
  font-size: 0.8em;
}
.assessment-period, .report-period{
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}
.period-item {
  flex-grow: 1;
  text-align: center;
}
.period-title {
  font-size: 1em;
}
.period-btn {
  border: 1px solid #a7a7a78a;
  border-radius: 5px;
}
.period-btn:hover {
  cursor: pointer;
  background: #a7a7a78a;
}
.period-btn:not(:last-of-type) {
  margin-right: 10px;
}
</style>