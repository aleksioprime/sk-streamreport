<template>
  <div class="block-filter">
    <div class="d-flex align-items-center flex-wrap mb-2">
      <div class="form-check me-2">
        <input class="form-check-input" type="radio" name="subject" :value="''" :id="'subject-x'" v-model="querySubject"
          @change="handleQuery">
        <label class="form-check-label" :for="'subject-x'">
          Все предметы
        </label>
      </div>
      <div v-for="sb in subjects" :key="sb.id" class="me-2">
        <div class="form-check">
          <input class="form-check-input" type="radio" name="subject" :value="sb.id" :id="'subject-' + sb.id"
            v-model="querySubject" @change="handleQuery">
          <label class="form-check-label" :for="'subject-' + sb.id">
            {{ sb.name_rus }}
          </label>
        </div>
      </div>
    </div>
    <div class="d-flex align-items-center" v-if="years.length > 0">
      <div class="me-2" v-for="year in years" :key="year.id">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" :value="year" :id="'year-' + year.id" v-model="queryYears"
            @change="handleQuery">
          <label class="form-check-label" :for="'year-' + year.id">
            <span v-if="year.id">{{ year.year_ib }}</span>
          </label>
        </div>
      </div>
      <div v-if="this.queryYears.length == 0" class="ms-auto">Показаны юниты всех лет</div>
      <div v-else class="ms-auto">Показан юниты выбранных лет</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    years: {
      type: Array,
      required: true,
      default: [],
    },
    subjects: {
      type: Array,
      required: true,
      default: [],
    },
  },
  setup(props) {
    return {
    }
  },
  data() {
    return {
      querySubject: '',
      queryYears: [],
    }
  },
  methods: {
    handleQuery(event) {
      const years = this.queryYears.map(item => item.id)
      this.$emit('updateFetch', { years: years, subject: this.querySubject });
    },
  },
  mounted() {
    console.log('Создание')
  },
  watch: {
    querySubject() {
      this.queryYears = [ ];
    },
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
}
</style>