<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Итоговые оценки по критериям</div>
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
          <div class="field-description">Поставьте оценки по критериям</div>
          <div class="criteria-wrapper">
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
            <button class="field-btn-done" @click="autoField">Автозаполнение</button>
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>

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
  data() {
    return {
      editMode: false,
      editData: {},
    }
  },
  methods: {
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData)
    },
    cancelField() {
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      this.editData.criterion_a = this.report.criterion_a;
      this.editData.criterion_b = this.report.criterion_b
      this.editData.criterion_c = this.report.criterion_c;
      this.editData.criterion_d = this.report.criterion_d;
    },
    autoField() {
      this.editData.criterion_a = this.avg_criteria.criterion_a;
      this.editData.criterion_b = this.avg_criteria.criterion_b;
      this.editData.criterion_c = this.avg_criteria.criterion_c;
      this.editData.criterion_d = this.avg_criteria.criterion_d;
    }
  },
}
</script>
<style>
.criteria-wrapper {
  display: flex;
  flex-wrap: wrap;
  column-gap: 10px;
  justify-content: space-between;
}
.criteria-item {
  margin-top: 10px;
  flex-basis: 23%;
  display: flex;
  align-items: center;
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
</style>