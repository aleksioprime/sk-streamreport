<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговое оценивание</template>
      <template v-slot:extra>
        <div class="toggle" v-if="isAdmin">
          <div class="toggle-item my">
            <input id="show-my" type="radio" :value="false" v-model="showAllData" @change="changeView">
            <label for="show-my">Мои оценки и репорты</label>
          </div>
          <div class="toggle-item all">
            <input id="show-all" type="radio" :value="true" v-model="showAllData" @change="changeView">
            <label for="show-all">Просмотр всех оценок и репортов</label>
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
        <select id="levels" class="form-select me-3 mb-2" v-model="currentLevel" @change="choiceProgram">
          <option v-for="(lvl, i) in levels" :key="i" :value="lvl.value">
            {{ lvl.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="block-class">
      <div class="radiobutton">
        <input type="radio" name="year" :value="null" id="year-null" v-model="currentYearId" @change="choiceYear">
        <label for="year-null">Все классы</label>
      </div>
      <div v-for="year in years" :key="year.id" class="radiobutton">
        <input type="radio" name="year" :value="year.id" :id="'year-' + year.id"
          v-model="currentYearId" @change="choiceYear">
        <label :for="'year-' + year.id">
          <div>{{ year.year_rus }} классы</div>
        </label>
      </div>
    </div>
    <!-- Выбор предмета -->
    <!-- <div class="my-2">
      <select ref="subject" id="grades" class="form-select" v-model="currentSubjectId">
        <option :value="null">Выберите предмет</option>
        <option v-for="(sb, i) in subjects" :key="i" :value="sb">
          {{ sb.name_rus }} ({{ sb.group_ib.name_eng }})
        </option>
      </select>
    </div> -->
    <div class="block-subject mt-3">
      <div class="subject radiobutton">
        <input type="radio" name="subject" :value="null" :id="'subject-x'" v-model="currentSubjectId"
          @change="choiceSubject">
        <label :for="'subject-x'">
          Предмет не выбран
        </label>
      </div>
      <div v-for="sb in subjects" :key="sb.id" class="subject radiobutton">
        <input type="radio" name="subject" :value="sb.id" :id="'subject-' + sb.id"
          v-model="currentSubjectId" @change="choiceSubject">
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
            <!-- <div class="assessment-wrapper" v-if="currentSubjectId">
              <div class="assessment-title">Итоговые оценки по предмету <b>{{ currentSubject.name_rus }}</b>:</div>
              <div class="assessment-period">
                <div class="period-item" :class="{'period-myp-item' : periodClass(year).length == 3}" v-for="period in periodClass(year)" :key="period.id" @click="$router.push(`/assessment/group/${group.id}/period/${period.id}/subject/${currentSubjectId}`)">
                  <div class="period-title">{{ period.number }} {{ period.type }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div> -->
            <div class="report-wrapper" v-if="currentSubjectId">
              <div class="report-title">Репорты учителя по предмету <b>{{ currentSubject.name_rus }}</b>:
              </div>
              <div class="report-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="openReportTeacher(group.id, period.id)">
                  <div class="period-title">{{ capitalizeString(period.name) }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div v-if="showAllData || authUser.teacher && group.psychologist && group.psychologist.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты психолога <span v-if="group.psychologist">({{ group.psychologist.user.last_name }} {{ group.psychologist.user.first_name }} {{ group.psychologist.user.middle_name }})</span>:</div>
              <div class="psychologist-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/psychologist/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">{{ capitalizeString(period.name) }}</div>
                  <div class="period-info"></div>
                </div>
              </div>
            </div>
            <div v-if="showAllData || authUser.teacher && group.mentor && group.mentor.id == authUser.teacher.id" class="mentor-wrapper" >
              <div class="report-title">Репорты наставника <span v-if="group.mentor">({{ group.mentor.user.last_name }} {{ group.mentor.user.first_name }} {{ group.mentor.user.middle_name }})</span>:</div>
              <div class="mentor-period">
                <div class="period-item" v-for="period in reportPeriods" :key="period.id"  @click="$router.push(`/report/mentor/group/${group.id}/period/${period.id}`)">
                  <div class="period-title">{{ capitalizeString(period.name) }}</div>
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
      currentSubjectId: null,
      currentLevel: 'ooo',
      levels: [
        { value: 'noo', name: 'Начальная школа' },
        { value: 'ooo', name: 'Средняя школа' },
        { value: 'soo', name: 'Старшая школа' },
      ],
      showAllData: false,
      currentYearId: null,
    }
  },
  methods: {
    capitalizeString(word) {
      return word.charAt(0).toUpperCase() + word.slice(1)
    },
    choiceProgram() {
      localStorage.setItem('assessment_level', this.currentLevel);
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: this.currentLevel }).finally(() => {
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id });
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id });
        if (this.showAllData) {
          this.fetchGetSubjects({ level: this.currentLevel, need_report: 1 });
          this.fetchGetClassYears({ level: this.currentLevel });
        } else {
          this.fetchGetSubjects({ teacher: this.authUser.teacher.id, level: this.currentLevel, need_report: 1 });
          this.fetchGetClassYears({ teacher: this.authUser.teacher.id, level: this.currentLevel });
        }
        this.currentSubjectId = null;
        localStorage.removeItem('assessment_subject');
        this.currentYearId = null;
        localStorage.removeItem('assessment_year');
      });
    },
    
    choiceSubject() {
      if (this.currentSubjectId) {
        localStorage.setItem('assessment_subject', this.currentSubjectId);
      } else {
        localStorage.removeItem('assessment_subject');
      }
    },
    choiceYear() {
      if (this.currentYearId) {
        localStorage.setItem('assessment_year', this.currentYearId);
      } else {
        localStorage.removeItem('assessment_year');
      }
    },
    changeView() {
      this.currentSubjectId = null;
      localStorage.removeItem('assessment_subject');
      this.currentYearId = null;
      localStorage.removeItem('assessment_year');
      if (this.showAllData) {
        localStorage.setItem('assessment_all', true);
      } else {
        localStorage.removeItem('assessment_all');
      }
    },
    openReportTeacher(group_id, period_id) {
      if (this.showAllData) {
        this.$router.push(`/report/teacher/group/${group_id}/period/${period_id}/subject/${this.currentSubjectId}`)
      } else {
        this.$router.push(`/report/teacher/group/${group_id}/period/${period_id}/subject/${this.currentSubjectId}/author/${this.authUser.teacher.id}`)
      }
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
    recoveryDataFromLocalStorage() {
      this.currentSubjectId = Number(localStorage.getItem('assessment_subject')) || null;
      this.currentLevel = localStorage.getItem('assessment_level') || 'MYP';
      this.currentYearId = Number(localStorage.getItem('assessment_year')) || null;
      this.showAllData = Boolean(localStorage.getItem('assessment_all')) || false;
    }
  },
  mounted() {
    // if (this.isAdmin) {
    //   this.showAllData = true;
    // }
    this.fetchGetStudyYears();
    this.recoveryDataFromLocalStorage();
    if (this.showAllData) {
      this.fetchGetSubjects({ level: this.currentLevel, need_report: 1 }).finally();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: this.currentLevel }).finally(() => {
        this.fetchGetClassYears({ level: this.currentLevel });
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
      });
    } else {
      this.fetchGetSubjects({ teacher: this.authUser.teacher.id, level: this.currentLevel, need_report: 1 }).finally();
      this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: this.currentLevel }).finally(() => {
        this.fetchGetClassYears({ teacher: this.authUser.teacher.id, level: this.currentLevel });
        this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
        this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
      });
    }
  },
  computed: {
    filteredGroups() {
      return this.groups.filter(item => {
        if (this.currentYearId) {
          if (this.showAllData) {
            return item.class_year.id == Number(this.currentYearId) 
          } else {
            return (item.class_year.id == Number(this.currentYearId) ) && (item.mentor.id == this.authUser.teacher.id || (item.psychologist.id == this.authUser.teacher.id) || this.currentSubjectId);
          }
        }
        return (this.currentSubjectId) || (item.mentor.id == this.authUser.teacher.id) || (item.psychologist.id == this.authUser.teacher.id);
      });
    },
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
    currentSubject() {
      return this.subjects.find(item => item.id == this.currentSubjectId)
    }
  },
  watch: {
    showAllData() {
      if (this.showAllData) {
        this.fetchGetSubjects({ level: this.currentLevel, need_report: 1 });
        this.fetchGetGroups({ study_year: this.currentStudyYear.id, level: this.currentLevel }).finally(() => {
          this.fetchGetClassYears({ level: this.currentLevel });
          this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
          this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
        });
      } else {
        this.fetchGetSubjects({ teacher: this.authUser.teacher.id, level: this.currentLevel, need_report: 1 });
        this.fetchGetGroups({ teacher: this.authUser.teacher.id, study_year: this.currentStudyYear.id, level: this.currentLevel }).finally(() => {
          this.fetchGetClassYears({ teacher: this.authUser.teacher.id, level: this.currentLevel });
          this.fetchGetPeriods({ study_year: this.currentStudyYear.id })
          this.fetchGetReportPeriods({ study_year: this.currentStudyYear.id })
        });
      }
    },
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