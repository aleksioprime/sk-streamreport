<template>
  <div v-if="units.length > 0" ref="userlist">
    <!-- Список юнитов -->
    <transition-group name="unit-list">
      <div v-for="unit in units" :key="unit.id" class="unit-item">
        <div class="unit-header">
          <div class="unit-title"><a :href="`/myp/${unit.id}`">{{ unit.title }}</a></div>
          <small v-if="unit.subject && unit.class_year">{{ unit.subject.name_rus }}, {{ unit.class_year.year_ib }}
            {{ unit.class_year.program }} ({{ getHours(unit.hours) }})</small>
        </div>
        <div class="unit-concepts">
          <div v-for="kc in unit.key_concepts" :key="kc.id" class="unit-kc">{{ kc.name_eng }}</div>
          <div v-for="(rc, index) in unit.related_concepts" :key="rc.id" class="unit-rc">{{ rc.name_eng }}<span
              v-if="++index !== unit.related_concepts.length">,&nbsp;</span></div>
        </div>
        <div class="unit-gcontext" v-if="unit.global_context">
          {{ unit.global_context.name_eng }}
          (<span v-for="(exp, index) in unit.explorations" :key="exp.id" class="unit-rc">
            {{ exp.name_eng }}<span v-if="++index !== unit.explorations.length">,&nbsp;</span></span>)
        </div>
        <div class="unit-soi" v-if="unit.statement_inquiry" v-html="unit.statement_inquiry">
        </div>
        <div class="unit-atl" v-if="unit.atl_mapping.length">
            <div v-for="atl in unit.atl_mapping" :key="atl.id" class="atl-item">{{atl.atl.cluster.name_eng }}</div>
          </div>
        <div class="unit-footer">
          <div class="unit-criteria">
            <div v-for="cr in unit.criteria" :key="cr.id" class="criteria-item" :class="classCriteria(cr.letter)">{{
              cr.letter }}</div>
          </div>
          <div class="unit-authors">
            <div v-for="author in unit.authors" :key="author.id" class="authors-item">{{ author.user.last_name }} {{ author.user.first_name }} {{ author.user.middle_name }}</div>
          </div>
        </div>
      </div>
    </transition-group>
    <!-- Нумерация страниц -->
    <base-pagination :total="totalPages" :current="currentPage" :range="2" @change="nextPage" />
  </div>
  <div v-else>
    Данных нет
  </div>
</template>

<script>

export default {
  name: 'UnitMYPList',
  props: {
    units: {
      type: Array,
      required: true,
      default: [],
    },
    totalPages: {
      type: Number,
      default: 1,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
  },
  setup(props) {

    return {

    }
  },
  data() {
    return {

    }
  },
  methods: {
    nextPage(page) {
      this.$emit('changePage', page)
    },
    containsKey(obj, key) { return Object.keys(obj).includes(key) },
    hasSubject(unit) { return this.containsKey(unit, 'subject') },
    hasClassYear(unit) { return this.containsKey(unit, 'class_year') },
    classCriteria(letter) {
      if (letter.toLowerCase() == 'a') {
        return 'criteria-a'
      } else if (letter.toLowerCase() == 'b') {
        return 'criteria-b'
      } else if (letter.toLowerCase() == 'c') {
        return 'criteria-c'
      } else {
        return 'criteria-d'
      }
    },
    getHours(hours) {
      let value = Math.abs(hours) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${hours} часов`;
      if (number > 1 && number < 5) return `${hours} часа`;
      if (number == 1) return `${hours} час`;
      return `${hours} часов`;
    }
  },
  computed: {
    
  },
  mounted() {

  },
}
</script>
  
<style scoped>
.unit-item {
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
  border-radius: 10px;
  margin: 20px 0;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.unit-header {
  margin-bottom: 5px;
}

.unit-title {
  font-weight: 700;
  font-size: 1.2em;
}

.unit-title a {
  text-decoration: none;
  text-transform: uppercase;
  color:#CA4348;
}

.unit-concepts {
  display: flex;
  flex-wrap: wrap;
}

.unit-kc {
  margin-right: 10px;
  text-decoration: underline;
}

.unit-soi {
  position: relative;
  margin-left: 20px;
  color: #333334;
  padding: 10px 10px 5px 10px;
  position: relative;
}

.unit-soi:before {
  content: "\201C";
  font-family: serif;
  position: absolute;
  left: -20px;
  top: -5px;
  color: #BCBCBC;
  font-size: 50px;
  text-shadow: 1px 2px 0 white;
}

.unit-soi p {
  margin-bottom: 0px;
}

.unit-criteria {
  display: flex;
  max-width: 300px;
  column-gap: 5px;
  margin: 10px 0;
}

.criteria-item {
  border-radius: 5px;
  padding: 5px;
  width: 40px;
  text-align: center;
  font-weight: 700;
}

.criteria-a {
  color: #54C3DA;
  border: 1px solid #54C3DA;
}

.criteria-b {
  color: #a59a50;
  border: 1px solid #a59a50;
}

.criteria-c {
  color: #7AC11A;
  border: 1px solid #7AC11A;
}

.criteria-d {
  color: #CA4348;
  border: 1px solid #CA4348;
}
.unit-atl {
  border: 1px solid #dee2e6;
  border-left: none;
  border-right: none;
  padding: 5px;
}
.unit-footer {
  display: flex;
  align-items: center;
}
.unit-authors {
  margin-left: auto;
  font-style: italic;
}
</style>