<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговое оценивание</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentStudyYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>

    <!-- Выбор предмета -->
    <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubject">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb.id">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div>


    <div v-if="!isGroupLoading">
      <div v-for="(groupsByYear, year) in groupedArrayData(groups, ['class_year'])" :key="year">
        <div class="class-group">{{ year }} классы</div>
        <div v-for="group in groupsByYear" :key="group.id" class="class-item">
          <div>{{ group.class_year }}{{ group.letter }} класс ({{ getWordStudent(group.count) }})</div>
          <div class="class-btns">
            <div v-if="currentSubject">
              <button class="btn btn-success" @click="$router.push(`/assessment/year/${group.class_year}/period/${currentPeriod.id}/subject/${currentSubject}`)">Оценки</button>
              <button class="btn btn-primary" @click="$router.push(`/report/teacher/group/${group.id}/subject/${currentSubject}`)">Репорты</button>
            </div>
            <button class="btn btn-primary" 
            v-if="authUser && group.mentor && authUser.teacher.id == group.mentor.id">Наставник</button>
            <button class="btn btn-primary" v-if="authUser && group.psychologist && authUser.teacher.id == group.psychologist.id">Психолог</button>
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
import { mapGetters } from 'vuex';

export default {
  components: {
    
  },
  setup(props) {
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { groupedArrayData } = getGroupedArray();
    const { subjects, fetchGetSubjects } = getSubjects();
    const { periods, currentPeriod, fetchGetPeriods } = getPeriods();
    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      groups, isGroupLoading, fetchGetGroups,
      groupedArrayData,
      subjects, fetchGetSubjects,
      periods, currentPeriod, fetchGetPeriods
    }
  },
  data() {
    return {
      currentSubject: null,
      currentProgram: 'MYP',
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
  },
  mounted() {
    this.fetchGetStudyYears();
    this.fetchGetGroups({ study_year: this.currentStudyYear }).finally(() => {
      this.fetchGetPeriods({ study_year: this.currentStudyYear, program: this.currentProgram })
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
.class-item:hover {
 background: #a7a7a78a;
 cursor: pointer;
}
.class-btns {
  margin-top: 10px;
  display: flex;
}
.class-btns .btn {
  margin-right: 5px;
}
</style>