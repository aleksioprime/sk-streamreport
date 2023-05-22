<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговое оценивание</template>
      <template v-slot:extra>
        <div class="toggle" v-if="isAdmin">
          <div class="toggle-item my">
            <input id="show-my" type="radio" :value="false" v-model="showAllData">
            <label for="show-my">Мои</label>
          </div>
          <div class="toggle-item all">
            <input id="show-all" type="radio" :value="true" v-model="showAllData">
            <label for="show-all">Все</label>
          </div>
        </div>
      </template>
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
        <select id="programs" class="form-select me-3 mb-2" v-model="currentProgram" @change="choiceProgram">
          <option v-for="(pr, i) in programs" :key="i" :value="pr.value">
            {{ pr.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="block-class">
      <div class="radiobutton">
        <input type="radio" name="year" :value="null" id="year-null" v-model="queryYear" @change="changeYears">
        <label for="year-null">Все классы</label>
      </div>
      <div v-for="year in years" :key="year.id" class="radiobutton">
        <input type="radio" name="year" :value="year.id" :id="'year-' + year.id"
          v-model="queryYear" @change="changeYears">
        <label :for="'year-' + year.id">
          <div>{{ year.year_rus }} классы</div>
        </label>
      </div>
    </div>
    <!-- Выбор предмета -->
    <!-- <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubject">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div> -->
    <div class="block-subject mt-3">
      <div class="subject radiobutton">
        <input type="radio" name="subject" :value="null" :id="'subject-x'" v-model="currentSubject"
          @change="changeSubject">
        <label :for="'subject-x'">
          Предмет не выбран
        </label>
      </div>
      <div v-for="sb in subjects" :key="sb.id" class="subject radiobutton">
        <input type="radio" name="subject" :value="sb" :id="'subject-' + sb.id"
          v-model="currentSubject" @change="changeSubject">
        <label :for="'subject-' + sb.id">
          {{ sb.name_rus }}
        </label>
      </div>
    </div>

    <div v-if="!isGroupLoading">
      <div v-for="(groupsByYear, year) in groupedArrayData(filteredGroups, ['class_year', 'year_rus'])" :key="year">
        <div class="class-group"><h3>{{ year }} классы</h3></div>
        <div v-for="group in groupsByYear" :key="group.id" class="class-item area">
            <div class="row">
              <div class="col-sm">
                <div class="class-title selected"><h5>{{ group.class_year.year_rus }}{{ group.letter }} класс ({{ getWordStudent(group.count) }})</h5></div>
              </div>
            </div>
            <div class="assessment-wrapper" v-if="currentSubject">
              <div class="assessment-title">Итоговые оценки по предмету <b>{{ currentSubject.name_rus }}</b>:</div>
              <div class="assessment-period">
                <div class="period-item" :class="{'period-myp-item' : periodClass(year).length == 3}" v-for="period in periodClass(year)" :key="period.id" @click="$router.push(`/assessment/group/${group.id}/period/${period.id}/subject/${currentSubject.id}`)">
                  <div class="period-title">Оценки за {{ period.number }} {{ period.type }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div class="report-wrapper" v-if="currentSubject">
              <div class="report-title">Репорты учителя по предмету <b>{{ currentSubject.name_rus }}</b>:
              </div>
              <div class="report-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/teacher/group/${group.id}/period/${period.id}/subject/${currentSubject.id}/`)">
                  <div class="period-title">Репорты за {{ period.name }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div v-if="showAllData || authUser.teacher && group.psychologist && group.psychologist.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты психолога <span v-if="group.psychologist">({{ group.psychologist.user.last_name }} {{ group.psychologist.user.first_name }} {{ group.psychologist.user.middle_name }})</span>:</div>
              <div class="psychologist-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/psychologist/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">Репорты за {{ period.name }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div v-if="showAllData || authUser.teacher && group.mentor && group.mentor.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты наставника <span v-if="group.mentor">({{ group.mentor.user.last_name }} {{ group.mentor.user.first_name }} {{ group.mentor.user.middle_name }})</span>:</div>
              <div class="mentor-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/mentor/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">Репорты за {{ period.name }}</div>
                  <div class="period-info"></div>
                </div>
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
import { getClassYears } from "@/hooks/unit/useClassYear";

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
    const { years, fetchGetClassYears } = getClassYears();

    return {
      studyYears, currentStudyYear, fetchGetStudyYears,
      groups, isGroupLoading, fetchGetGroups,
      groupedArrayData,
      subjects, fetchGetSubjects,
      periods, fetchGetPeriods,
      reportPeriods, currentReportPeriod, fetchGetReportPeriods,
      years, fetchGetClassYears
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
      ],
      showAllData: false,
      queryYear: null,
    }
  },
  methods: {
    choiceProgram() {
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, program: this.currentProgram }).finally(() => {
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        if (this.showAllData) {
          this.fetchGetSubjects({ program: this.currentProgram });
          this.fetchGetClassYears({ program: this.currentProgram });
        } else {
          this.fetchGetSubjects({ teacher: this.authUser.teacher.id, program: this.currentProgram });
          this.fetchGetClassYears({ teacher: this.authUser.teacher.id, program: this.currentProgram });
        }
        this.currentSubject = null;
      });
    },
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
    // if (this.isAdmin) {
    //   this.showAllData = true;
    // }
    this.fetchGetStudyYears();
    if (this.showAllData) {
      this.fetchGetSubjects({ program: this.currentProgram });
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, program: this.currentProgram }).finally(() => {
        this.fetchGetClassYears({ program: this.currentProgram });
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
      });
    } else {
      this.fetchGetSubjects({ teacher: this.authUser.teacher.id, program: this.currentProgram });
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, program: this.currentProgram }).finally(() => {
        this.fetchGetClassYears({ teacher: this.authUser.teacher.id, program: this.currentProgram });
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
      });
    }
  },
  computed: {
    filteredGroups() {
      return this.groups.filter(item => {
        if (this.queryYear) {
          if (this.showAllData) {
            return item.class_year.id == Number(this.queryYear) 
          } else {
            return (item.class_year.id == Number(this.queryYear) ) && (item.mentor.id == this.authUser.teacher.id || (item.psychologist.id == this.authUser.teacher.id) || this.currentSubject);
          }
        }
        return (this.currentSubject) || (item.mentor.id == this.authUser.teacher.id) || (item.psychologist.id == this.authUser.teacher.id);
      });
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  watch: {
    showAllData() {
      if (this.showAllData) {
        this.fetchGetSubjects({ program: this.currentProgram });
        this.fetchGetGroups({ study_year: this.currentStudyYear.id, program: this.currentProgram }).finally(() => {
          this.fetchGetClassYears({ program: this.currentProgram });
          this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
          this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
        });
      } else {
        this.fetchGetSubjects({ teacher: this.authUser.teacher.id, program: this.currentProgram });
        this.fetchGetGroups({ teacher: this.authUser.teacher.id, study_year: this.currentStudyYear.id, program: this.currentProgram }).finally(() => {
          this.fetchGetClassYears({ teacher: this.authUser.teacher.id, program: this.currentProgram });
          this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
          this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
        });
      }
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';
.block-class {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 5px;
  margin-bottom: 10px;
}
.class-title {
  font-weight: 700;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
.class-title h5 {
  margin-bottom: 0;
}
.class-group {
  text-transform: uppercase;
  font-size: 1.5em;
  margin-top: 10px;
}
.class-item {
  padding: 10px;
  margin-top: 5px;
  display: flex;
  flex-direction: column;
}
.class-btns {
  margin-top: 10px;
  display: flex;
}
.class-btns .btn {
  margin-right: 5px;
}
.assessment-wrapper {
  margin-top: 10px;
}
.assessment-title, .report-title {
  font-size: 0.8em;
}
.assessment-period, .report-period, .mentor-period, .psychologist-period{
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  row-gap: 5px;
  margin: 10px 0;
}
.period-myp-item {
  flex-basis: 33% !important;
}
.period-item {
  flex-basis: 49%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #a7a7a78a;
}
.period-item:hover {
  cursor: pointer;
  transition: 1s;
  background: #a7a7a78a;
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
.report-wrapper {
  margin-top: 0;
}

</style>