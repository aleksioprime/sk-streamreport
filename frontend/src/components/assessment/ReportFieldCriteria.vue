<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Итоговые баллы по критериям</div>
      <button v-if="!editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div class="criteria-wrapper">
            <div class="criteria-item">
              <div class="criteria-a">{{ criteria.criterion_a.letter }}. {{ criteria.criterion_a.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_a || '-' }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-b">{{ criteria.criterion_b.letter }}. {{ criteria.criterion_b.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_b || '-' }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-c">{{ criteria.criterion_c.letter }}. {{ criteria.criterion_c.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_c || '-' }}</div>
            </div>
            <div class="criteria-item">
              <div class="criteria-d">{{ criteria.criterion_d.letter }}. {{ criteria.criterion_d.name_eng }}</div>
              <div class="criteria-value">{{ this.report.criterion_d || '-' }}</div>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="field-description">Выставите итоговые баллы по критериям вашей предметной области <b>{{ report.subject.group_ib.name_eng }}</b></div>
          <div class="achievements-title selected" data-bs-toggle="collapse" :href="`#collapse-achievements-${report.id}`" role="button" aria-expanded="false" :aria-controls="`collapse-achievements-${report.id}`">
            Выставление баллов по предметным достижениям
          </div>
          <div :id="`collapse-achievements-${report.id}`" class="collapse">
            <div class="row">
              <div class="criterion-wrapper col-sm mt-2">
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_a" id="criterion_a" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_a" class="criterion-a">A</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_b" id="criterion_b" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_b" class="criterion-b">B</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_c" id="criterion_c" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_c" class="criterion-c">C</label>
                </div>
                <div class="radiobutton">
                  <input type="radio" name="criteria" :value="criteria.criterion_d" id="criterion_d" v-model="currentCriterion" @change="changeCriterion">
                  <label for="criterion_d" class="criterion-d">D</label>
                </div>
              </div>
              <div class="col-sm-4 mt-2">
                <select class="form-select" name="level-subject" id="level-subject" v-model="currentYear" @change="changeYear">
                  <option :value="{}">Выберите уровень</option>
                  <option v-for="lvl in levels" :key="lvl.id" :value="lvl">{{ lvl.name_eng }}</option>
                </select>
              </div>
            </div>
            <div class="achievements-wrapper">
              <div v-if="currentCriterion.id && currentYear.id">
                <div class="achievements-filter">
                  <div>Уровни достижений по критерию <b>{{ this.currentCriterion.letter }}. {{ this.currentCriterion.name_eng }}</b> за <b>{{ currentYear.name_eng }}</b>:</div>
                </div>
                <div class="accordion" :id="`accordion-${currentCriterion.id}`">
                  <div class="accordion-item" v-for="objective in filteredObjectivesByYearAndCriterion" :key="objective.id">
                    <h2 class="accordion-header">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-objective-${objective.id}`" aria-expanded="true" :aria-controls="`collapse-objective-${objective.id}`">
                        {{ objective.strand.letter_i }}. {{ objective.name_eng }}
                      </button>
                    </h2>
                    <div :id="`collapse-objective-${objective.id}`" class="accordion-collapse collapse" :data-bs-parent="`#accordion-${currentCriterion.id}`">
                      <div class="accordion-body">
                        <div v-if="objective.achievelevel.length">
                          <div class="radio-check">
                            <input type="radio" :name="`achievement-${objective.id}`" :value="null" :id="`achievement-${objective.id}-none`" v-model="currentAchievement[`${objective.id}`]">
                            <label :for="`achievement-${objective.id}-none`" class="achievement-item">
                              <div class="achievement-name">Стрэнд не участвует в оценке</div>
                              <div class="achievement-point">-</div>
                            </label>
                          </div>
                          <div class="radio-check">
                            <input type="radio" :name="`achievement-${objective.id}`" :value="0" :id="`achievement-${objective.id}-0`" v-model="currentAchievement[`${objective.id}`]">
                            <label :for="`achievement-${objective.id}-0`" class="achievement-item">
                              <div class="achievement-name">The student does not reach a standard described by any of the descriptors below</div>
                              <div class="achievement-point">0</div>
                            </label>
                          </div>
                          <div v-for="ach in objective.achievelevel" :key="ach.id">
                            <div class="radio-check">
                              <input type="radio" :name="`achievement-${objective.id}`" :value="ach.id" :id="`achievement-${objective.id}-${ach.id}`" v-model="currentAchievement[`${objective.id}`]">
                              <label :for="`achievement-${objective.id}-${ach.id}`" class="achievement-item">
                                <div class="achievement-name">The student {{ ach.name_eng }}</div>
                                <div class="achievement-point">{{ ach.point - 1 }} - {{ ach.point }}</div>
                              </label>
                            </div>
                          </div>
                        </div>
                        <div v-else>Нет данных</div>
                      </div> 
                    </div>
                  </div>
                  <button class="field-btn-done mt-2" @click="saveAchievementField">Сохранить и рассчитать</button>
                </div>
              </div>
            </div>         
            <div>Рассчитанные баллы по предметным достижениям:</div>
            <div class="criteria-wrapper predict">
              <div class="criteria-item predict">
                <div class="criteria-a">{{ criteria.criterion_a.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('A') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-b">{{ criteria.criterion_b.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('B') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-c">{{ criteria.criterion_c.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('C') }}</div>
              </div>
              <div class="criteria-item">
                <div class="criteria-d">{{ criteria.criterion_d.letter }}: </div>
                <div class="criteria-value">{{ getPredictCriteriaMark('D') }}</div>
              </div>
            </div>       
          </div>
          <div class="criteria-wrapper edit">
            <div class="criteria-item">
              <label for="criteria-a">{{ criteria.criterion_a.letter }}. {{ criteria.criterion_a.name_eng }}</label>
              <input id="criteria-a" class="form-control" type="number" v-model="editData.criterion_a" inputmode="decimal" maxlength="1" min="0" max="8">
            </div>
            <div class="criteria-item">
              <label for="criteria-b">{{ criteria.criterion_b.letter }}. {{ criteria.criterion_b.name_eng }}</label>
              <input id="criteria-b" class="form-control" type="number" v-model="editData.criterion_b" inputmode="decimal" maxlength="1" min="0" max="8">
            </div>
            <div class="criteria-item">
              <label for="criteria-c">{{ criteria.criterion_c.letter }}. {{ criteria.criterion_c.name_eng }}</label>
              <input id="criteria-c" class="form-control" type="number" v-model="editData.criterion_c" inputmode="decimal" maxlength="1" min="0" max="8">
            </div>
            <div class="criteria-item">
              <label for="criteria-d">{{ criteria.criterion_d.letter }}. {{ criteria.criterion_d.name_eng }}</label>
              <input id="criteria-d" class="form-control" type="number" v-model="editData.criterion_d" inputmode="decimal" maxlength="1" min="0" max="8">
            </div>
          </div>
          <div class="field-buttons">
            <button class="field-btn-done" @click="autoFieldPeriod">Auto: периоды</button>
            <button class="field-btn-done" @click="autoFieldAchievement">Auto: достижения</button>
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
import { getObjectives } from "@/hooks/unit/useObjective";
import { getLevels } from "@/hooks/unit/useLevel";

export default {
  name: 'ReportFieldCriteria',
  props: {
    report: { 
      type: Object, 
      default: {}
    },
    criteria: {
      type: Object,
    },
    avg_criteria: {
      type: Object,
    }
  },
  setup(props) {
    const { objectives, fetchGetObjectives } = getObjectives();
    const { levels, fetchGetLevels } = getLevels();
    return {
      objectives, fetchGetObjectives,
      levels, fetchGetLevels,
    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
      currentYear: {},
      currentCriterion: {},
      currentAchievement: {}
    }
  },
  methods: {
    getPredictCriteriaMark(criterion) {
      let answer = null
      if (criterion == 'A') {
        answer = this.report.predict[this.criteria.criterion_a.id].sum_points / this.report.predict[this.criteria.criterion_a.id].all_strands
      } else if (criterion == 'B') {
        answer = this.report.predict[this.criteria.criterion_b.id].sum_points / this.report.predict[this.criteria.criterion_b.id].all_strands
      } else if (criterion == 'C') {
        answer = this.report.predict[this.criteria.criterion_c.id].sum_points / this.report.predict[this.criteria.criterion_c.id].all_strands
      } else if (criterion == 'D') {
        answer = this.report.predict[this.criteria.criterion_d.id].sum_points / this.report.predict[this.criteria.criterion_d.id].all_strands
      } else {
        return 'E'
      }
      return answer ? Math.round(answer) : null
    },
    getCurrentAchievement() {
      this.filteredObjectivesByYear.forEach((item) => {
        const findedAchievement = this.report.achievements.find(obj => item.id == obj.objective && obj.level == this.currentYear.id)
        if (findedAchievement) {
          if (findedAchievement.achievement) {
            this.currentAchievement[`${item.id}`] = findedAchievement.achievement
          } else {
            this.currentAchievement[`${item.id}`] = 0
          }
        } else {
          this.currentAchievement[`${item.id}`] = null
        }
      })
    },
    changeYear() {
      this.currentAchievement = {}
    },
    changeCriterion() {
    },
    saveField() {
      this.editMode = false;
      for (let key in this.editData) {
        this.editData[key] = this.setValidMark(this.editData[key])
      }
      this.$emit('save', this.editData);
    },
    saveAchievementField() {
      const fetchData = {
        achievements: []
      }
      for (let key in this.currentAchievement) {
        if (this.currentAchievement[key] == 0) {
          fetchData.achievements.push({ objective_id: key })
        } else if (this.currentAchievement[key] != null) {
          fetchData.achievements.push({ objective_id: key, achievement_id: this.currentAchievement[key] })
        }
      }
      console.log(fetchData);
      this.$emit('save', fetchData);
    },
    cancelField() {
      this.objectives = [];
      this.currentAchievement = {};
      this.currentCriterion = {};
      this.editMode = false;
    },
    setValidMark(rawMark) {
      if (rawMark > 8) {
        return 8
      } else if (rawMark > 0 && rawMark < 8) {
        return Number(rawMark)
      } else if (rawMark < 0) {
        return 0
      } else {
        return null
      }
    },
    editField() {
      this.editMode = true;
      this.editData.criterion_a = this.report.criterion_a;
      this.editData.criterion_b = this.report.criterion_b
      this.editData.criterion_c = this.report.criterion_c;
      this.editData.criterion_d = this.report.criterion_d;
      this.fetchGetLevels({ subject: this.$route.params.id_subject }).finally(() => {
        if (this.report.subject.group_ib.id != 2) {
          this.currentYear = this.levels.find(item => item.name_eng == this.report.year.year_ib)
        } else {
          if (this.report.year.year_ib == 'Year 1' || this.report.year.year_ib == 'Year 2') {
            this.currentYear = this.levels.find(item => item.name_eng == 'Emergent')
          } else if (this.report.year.year_ib == 'Year 3' || this.report.year.year_ib == 'Year 4') {
            this.currentYear = this.levels.find(item => item.name_eng == 'Capable')
          } else {
            this.currentYear = this.levels.find(item => item.name_eng == 'Proficient')
          }
        }
        this.fetchGetObjectives({ subject: this.$route.params.id_subject }).finally(() => {
          this.getCurrentAchievement();
          this.currentCriterion = this.criteria.criterion_a
        })
      });
    },
    autoFieldPeriod() {
      this.editData.criterion_a = this.avg_criteria.criterion_a;
      this.editData.criterion_b = this.avg_criteria.criterion_b;
      this.editData.criterion_c = this.avg_criteria.criterion_c;
      this.editData.criterion_d = this.avg_criteria.criterion_d;
    },
    autoFieldAchievement() {
      this.editData.criterion_a = this.getPredictCriteriaMark('A');
      this.editData.criterion_b = this.getPredictCriteriaMark('B');
      this.editData.criterion_c = this.getPredictCriteriaMark('C');
      this.editData.criterion_d = this.getPredictCriteriaMark('D');
    }
  },
  computed: {
    filteredObjectivesByYear() {
      return this.objectives.filter(item => item.level.id == this.currentYear.id)
    },
    filteredObjectivesByYearAndCriterion() {
      return this.filteredObjectivesByYear.filter(item => item.strand.criterion.id == this.currentCriterion.id)
    }
  }
}
</script>
<style scoped>
.criteria-wrapper {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  row-gap: 10px;
  justify-content: space-between;
}
.criteria-wrapper.edit {
  border: 1px solid var(--bs-secondary);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
}
.criteria-wrapper.predict {
  border: 1px solid var(--my-focus);
  margin-top: 10px;
  border-radius: 5px;
  padding: 10px;
  flex-wrap: nowrap;
}
.criteria-item {
  flex-basis: 23%;
  display: flex;
  align-items: center;
}
.criteria-wrapper.predict .criteria-value {
  margin-left: 10px;
  width: 100%;
}
.criteria-item input {
  width: 70px;
}
.criteria-item label {
  width: 100%;
  margin-right: 10px;
}
.criteria-value {
  border: 1px solid #a7a7a78a;
  padding: 5px 10px;
  margin-left: auto;
  min-height: 40px;
  border-radius: 5px;
  min-width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
@media screen and (max-width: 992px) {
  .criteria-item {
    flex-basis: 45%;
  }
}
.criterion-wrapper {
  display: flex;
  column-gap: 5px;
}
.criterion-wrapper div:hover {
  background: var(--my-focus) !important;
  cursor: pointer;
}
.accordion-button{
  padding: 10px;
}
.achievements-wrapper {
  flex-grow: 1;
  margin-bottom: 10px;
}
.achievements-filter {
  margin: 10px 0;
  display: flex;
  align-items: center;
  /* padding: 10px 0; */
  border-radius: 10px;
}
.achievements-title {
  padding: 10px;
  border-radius: 5px;
}
.achievements-filter select{
  margin-left: 10px;
  max-width: 200px;
}
.achievement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  column-gap: 10px;
  font-size: 0.8em;
}
.achievement-point {
  min-width: 100px;
  padding: 5px;
  border: 0.5px solid #a7a7a78a;
  text-align: center;
}
.radiobutton input[type=radio]:checked + label.criterion-a {
	background: #F26728 !important;
}
.radiobutton input[type=radio]:checked + label.criterion-b {
	background: #CDDC29 !important;
}
.radiobutton input[type=radio]:checked + label.criterion-c {
	background: #5C2D85 !important;
  color: #fff !important;
}
.radiobutton input[type=radio]:checked + label.criterion-d {
	background: #FED107 !important;
}
.radiobutton label {
  font-size: 1em;
}

/* Кнопки из радиокнопок */
.radio-check input[type=radio] {
	display: none;
}
.radio-check label {
  height: 100%;
  display: flex;
	cursor: pointer;
	padding: 10px;
	border: 1px solid #999;
	border-radius: 10px;
	user-select: none;
}
 
.radio-check input[type=radio]:checked + label {
	background: var(--my-focus);
  color: #000
}

.radio-check label:hover {
	color: #666;
}
.accordion-body {
  padding: 10px;
}
.field-buttons {
  display: flex;
  flex-wrap: wrap;
  row-gap: 5px;
}
@media screen and (max-width: 992px) {
  .field-buttons button {
    flex-basis: 45%;
  }
}
</style>