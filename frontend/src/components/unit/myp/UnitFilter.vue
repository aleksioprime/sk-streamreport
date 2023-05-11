<template>
  <div class="block-filter">
    <div v-if="showAllUnits">
      <div class="block-departments">
        <div v-for="dp in departments" :key="dp.id" class="department">
          <input type="radio" name="department" :value="dp.id" :id="'department-' + dp.id"
            v-model="queryDepartment" @change="handleQuery">
          <label :for="'department-' + dp.id">
            <img :src='dp.photo ? dp.photo : require("@/assets/img/user.png")' alt="" width="50" height="50">
            <div>{{ dp.name }}</div>
          </label>
        </div>
      </div>
    </div>
    <div class="d-flex align-items-center flex-wrap mb-2">
      <div class="form-check me-2">
        <input class="form-check-input" type="radio" name="subject" :value="null" :id="'subject-x'" v-model="querySubject"
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
    <div class="d-flex align-items-center year-filter" v-if="years.length > 0" :class="{ 'filter-active' : this.queryYears.length }">
      <div class="me-2" v-for="year in years" :key="year.id">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" :value="year.id" :id="'year-' + year.id" v-model="queryYears"
            @change="handleQuery">
          <label class="form-check-label" :for="'year-' + year.id">
            <span v-if="year.id">{{ year.year_ib }}</span>
          </label>
        </div>
      </div>
      <!-- <div v-if="this.queryYears.length == 0" class="ms-auto">Показаны юниты всех лет</div>
      <div v-else class="ms-auto">Показан юниты выбранных лет</div> -->
    </div>
  </div>
</template>

<script>
import { getDepartments } from "@/hooks/user/useDepartment";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getSubjects } from "@/hooks/curriculum/useSubject";

export default {
  props: {
    showAllUnits: {
      type: Boolean,
      default: false,
    },
    user: {
      type: Object
    },
  },
  setup(props) {
    const { departments, fetchGetDepartments } = getDepartments();
    const { years, fetchGetClassYears } = getClassYears();
    const { subjects, fetchGetSubjects } = getSubjects();

    return {
      departments, fetchGetDepartments,
      years, fetchGetClassYears,
      subjects, fetchGetSubjects,
    }
  },
  data() {
    return {
      querySubject: null,
      queryYears: [],
      queryDepartment: null,
    }
  },
  methods: {
    handleQuery(event) {
      
      this.$emit('updateFetch', { years: this.queryYears, subject: this.querySubject, department: this.queryDepartment });
    },
  },
  mounted() {
    this.fetchGetClassYears({ teacher: this.user.teacher.id, program: 'MYP' }).finally(() => {
      // this.queryYears = this.years.map(item => item.id);
    });
    this.fetchGetSubjects({ teacher: this.user.teacher.id, program: 'MYP' });
  },
  watch: {
    querySubject() {
      // this.queryYears = this.years.map(item => item.id)
    },
    queryDepartment() {
      this.querySubject = null;
      this.fetchGetSubjects({ department: this.queryDepartment, program: 'MYP' });
      // this.queryYears = this.years.map(item => item.id);
    },
    showAllUnits() {
      if (this.showAllUnits) {
        console.log('Включён режим администратора');
        this.fetchGetDepartments();
        this.fetchGetClassYears({ program: 'MYP' }).finally(() => {
          // this.queryYears = this.years.map(item => item.id);
        });
        this.queryDepartment = null;
        this.fetchGetSubjects({ department: this.queryDepartment, program: 'MYP' }); 
        this.handleQuery();
      } else {
        this.fetchGetSubjects({ teacher: this.user.teacher.id, program: 'MYP' }); 
        this.fetchGetClassYears({ teacher: this.user.teacher.id, program: 'MYP' }).finally(() => {
          // this.queryYears = this.years.map(item => item.id);
        });
      }
    }
  }
}
</script>

<style>
.block-filter {
  border: 1px solid #ced4da;
  padding: 10px;
}
.block-departments {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
  gap: 5px;
  margin-bottom: 10px;
}
.department {
	flex-basis: 10%;
  flex-grow: 1;
}
@media (max-width: 992px) {
  .department {
    flex-basis: 18%;
  }
}
.department img {
  margin-bottom: 10px;
}
.department input[type=radio] {
	display: none;
}
.department label {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  /* justify-content: space-between; */
	cursor: pointer;
	padding: 10px;
	border: 1px solid #999;
	border-radius: 6px;
	user-select: none;
  font-size: 0.8em;
}
 
/* Checked */
.department input[type=radio]:checked + label {
	background: #ffe0a6;
}
 
/* Hover */
.department label:hover {
	color: #666;
}
.year-filter {
  border: 1px solid #999;
  border-radius: 6px;
  padding: 10px;
}
.filter-active {
  background: #ffe0a6;
}
</style>