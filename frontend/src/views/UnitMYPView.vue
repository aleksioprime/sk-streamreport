<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/myp">Вернуться к списку юнитов</a></template>
      <template v-slot:header>Работа с юнитпланером MYP</template>
    </base-header>
    <transition name="fade">
      <div class="row" v-if="!isUnitLoading">
        <div class="col-sm-4">
          <nav id="navbar-myp" class="navbar-myp">
            <nav class="nav nav-pills flex-column">
              <a class="nav-link myp-group" href="#myp-base">Основная информация</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('title')" href="#title">Название юнита</a>
                <a class="nav-link myp-field" :class="checkField('subject')" href="#subject">Предмет</a>
                <a class="nav-link myp-field" :class="checkField('authors')" href="#authors">Учителя</a>
                <a class="nav-link myp-field" :class="checkField('class_year')" href="#class_year">Год обучения</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-inquiry">Исследование</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('key_concepts')" href="#key_concepts">Ключевые концепты</a>
                <a class="nav-link myp-field" :class="checkField('related_concepts')" href="#related_concepts">Предметные концепты</a>
                <a class="nav-link myp-field" :class="checkField('conceptual_understanding')" href="#conceptual_understanding">Концептуальное понимание</a>
                <a class="nav-link myp-field" :class="checkField('global_context')" href="#global_context">Глобальный контекст</a>
                <a class="nav-link myp-field" :class="checkField('explorations')" href="#explorations">Линии исследования</a>
                <a class="nav-link myp-field" :class="checkField('statement_inquiry')" href="#statement_inquiry">Формулировка исследования</a>
                <a class="nav-link myp-field" :class="checkField('inquiry_questions')" href="#inquiry_questions">Исследовательские вопросы</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-objectives">Образовательные цели</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('aims')" href="#aims">Общие цели</a>
                <a class="nav-link myp-field" :class="checkField('criteria')" href="#criteria">Критерии оценивания</a>
                <a class="nav-link myp-field" :class="checkField('strands')" href="#strands">Цели предметной группы</a>
                <a class="nav-link myp-field" :class="checkField('content')" href="#content">Содержание</a>
                <a class="nav-link myp-field" :class="checkField('skills')" href="#skills">Умения</a>
                <a class="nav-link myp-field" :class="checkField('atl_mapping')" href="#atl_mapping">Карта ATL</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-profile">Профиль студента</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('learner_profile')" href="#learner_profile">Профиль студента IB</a>
                <a class="nav-link myp-field" :class="checkField('international_mindedness')" href="#international_mindedness">Межкультурное понимание</a>
                <a class="nav-link myp-field" :class="checkField('academic_integrity')" href="#academic_integrity">Академическая честность</a>
                <a class="nav-link myp-field" :class="checkField('language_development')" href="#language_development">Языковое развитие</a>
                <a class="nav-link myp-field" :class="checkField('infocom_technology')" href="#infocom_technology">Использование средств ИКТ</a>
                <a class="nav-link myp-field" :class="checkField('service_as_action')" href="#service_as_action">Служение как действие</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-assessment">Оценивание</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('formative_assessment')" href="#formative_assessment">Текущее оценивание</a>
                <a class="nav-link myp-field" :class="checkField('summative_assessment_task')" href="#summative_assessment_task">Итоговое оценивание (задания)</a>
                <a class="nav-link myp-field" :class="checkField('summative_assessment_soi')" href="#summative_assessment_soi">Итоговое оценивание (взаимосвязь с
                  исследовательским утверждением)</a>
                <a class="nav-link myp-field" :class="checkField('peer_self_assessment')" href="#peer_self_assessment">Взаимное и самооценивание</a>
                <a class="nav-link myp-field" :class="checkField('standardization_moderation')" href="#standardization_moderation">Стандартизация и модерация</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-teaching">Стратегии преподавания</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('prior_experiences')"  href="#prior_experiences">Предыдущий опыт обучения</a>
                <a class="nav-link myp-field" :class="checkField('learning_experiences')" href="#learning_experiences">Учебная деятельность</a>
                <a class="nav-link myp-field" :class="checkField('teaching_strategies')" href="#teaching_strategies">Стратегии преподавания</a>
                <a class="nav-link myp-field" :class="checkField('student_expectations')" href="#student_expectations">Ожидания студентов</a>
                <a class="nav-link myp-field" :class="checkField('differentiation')" href="#differentiation">Дифференциация</a>
                <a class="nav-link myp-field" :class="checkField('resources')" href="#resources">Ресурсы</a>
              </nav>
              <a class="nav-link myp-group" href="#myp-reflections">Рефлексия</a>
              <nav class="nav nav-pills flex-sm-column">
                <a class="nav-link myp-field" :class="checkField('reflection_prior')"  href="#reflection_prior">До начала изучения</a>
                <a class="nav-link myp-field" :class="checkField('reflection_during')" href="#reflection_during">В процессе изучения юнита</a>
                <a class="nav-link myp-field" :class="checkField('reflection_after')" href="#reflection_after">По окончании изучения юнита</a>
              </nav>
            </nav>
          </nav>
        </div>
        <div class="col-sm">
          <div data-bs-spy="scroll" data-bs-target="#navbar-myp" data-bs-smooth-scroll="true" tabindex="0">
            <div id="myp-base"></div>
            <!-- Название юнита -->
            <unit-field-string id="title" :fieldName="'title'" :fieldText="fieldText.title" :fieldData="unitMYP.title"
              @save="unitFieldSave" />
            <!-- Год обучения -->
            <unit-field-select id="class_year" :fieldName="'class_year'" :fieldText="fieldText.class_year"
              :fieldData="unitMYP.class_year" :options="years" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
              <template v-slot:edit="field">{{ field.data.year_ib }} ({{ field.data.year_rus }} класс)</template>
            </unit-field-select>
            <div id="myp-inquiry"></div>
            <!-- Ключевой концепт -->
            <unit-field-checkbox id="key_concepts" :fieldName="'key_concepts'" :fieldText="fieldText.key_concepts"
              :fieldData="unitMYP.key_concepts" :options="keyConcepts" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}<br><small>
                {{ field.data.description_eng }}</small></template>
              <template v-slot:edit="field">
                <div :class="{ 'kc-recomend': checkKeyConcept(field.data) }"> {{ field.data.name_eng }}
                  (<span v-for="(rs, index) in field.data.recommended_subjects" :key="rs.id"><span v-if="index != 0">,
                  </span>{{ rs.name_eng }}</span>)</div>
              </template>
            </unit-field-checkbox>
            <unit-field-text id="conceptual_understanding" :fieldName="'conceptual_understanding'"
              :fieldText="fieldText.conceptual_understanding" :fieldData="unitMYP.conceptual_understanding"
              @save="unitFieldSave" />
            <!-- Глобальный контекст -->
            <unit-field-radio id="global_context" :fieldName="'global_context'" :fieldText="fieldText.global_context"
              :fieldData="unitMYP.global_context" :options="globalContexts" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:show="field">{{ field.data.name_eng }}</template>
              <template v-slot:edit="field">{{ field.data.name_eng }}<br>
                <small>{{ field.data.description_eng }}</small></template>
            </unit-field-radio>
            <!-- Предметные цели -->
            <unit-field-checkbox-grouped id="strands" :fieldName="'strands'" :fieldText="fieldText.strands" :fieldGroup="'criterion'"
              :fieldData="unitMYP.strands" :options="strands" @save="unitFieldSave" @edit="unitFieldEdit">
              <template v-slot:showGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:show="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
              <template v-slot:editGroup="field">
                {{ getCriteriaByID(field.data).letter }}. {{ getCriteriaByID(field.data).name_eng }}
              </template>
              <template v-slot:edit="field">{{ field.data.letter_i }}. {{ field.data.name_eng }}</template>
            </unit-field-checkbox-grouped>

          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import Editor from '@tinymce/tinymce-vue';
import fieldText from '@/assets/fieldstext.json'
import { getUnitMYP, updateUnitMYP } from "@/hooks/unit/useUnitMYP";
import { getClassYears } from "@/hooks/unit/useClassYear";
import { getKeyConcepts } from "@/hooks/unit/useKeyConcepts";
import { getGlobalContext } from "@/hooks/unit/useGlobalContext";
import { getStrands } from "@/hooks/unit/useStrand";

export default {
  name: 'UnitMYPView',
  components: {
    'editor': Editor
  },
  setup(props) {
    const { unitMYP, isUnitLoading, fetchGetUnitMYP } = getUnitMYP();
    const { updatedUnitMYP, fetchUpdateUnitMYP } = updateUnitMYP();
    const { years, fetchGetClassYears } = getClassYears();
    const { keyConcepts, fetchGetKeyConcepts } = getKeyConcepts();
    const { globalContexts, fetchGetGlobalContexts } = getGlobalContext();
    const { strands, fetchGetStrands } = getStrands();
    return {
      unitMYP, isUnitLoading, fetchGetUnitMYP,
      updatedUnitMYP, fetchUpdateUnitMYP,
      years, fetchGetClassYears,
      keyConcepts, fetchGetKeyConcepts,
      globalContexts, fetchGetGlobalContexts,
      strands, fetchGetStrands,
    }
  },
  data() {
    return {
      fieldText: fieldText,
      unitMYPEditing: {},
      iconUrl: "",
    }
  },
  methods: {
    unitFieldEdit(field) {
      if (field == 'key_concepts') {
        this.fetchGetKeyConcepts();
      } else if (field == 'class_year') {
        this.fetchGetClassYears({ program: 'MYP' });
      } else if (field == 'global_context') {
        this.fetchGetGlobalContexts();
      } else if (field == 'strands') {
        this.fetchGetStrands({ subject: this.unitMYP.subject.id, criteria: this.unitMYP.criteria.map(item => item.id)});
      }
    },
    unitFieldSave(unit) {
      console.log('Сохранение юнита: ', unit);
      this.fetchUpdateUnitMYP(this.$route.params.id, unit).finally(() => {
        this.unitMYP = { ...this.updatedUnitMYP }
      })
    },
    // Проверка ключевого концепта в качестве рекомендованного в предметной группе
    checkKeyConcept(field) {
      return field.recommended_subjects.filter(item => this.unitMYP.subject.group_ib.id == item.id).length;
    },
    // Получить критерий по ID из данных юнита
    getCriteriaByID(id) {
      return this.unitMYP.criteria.find(item => item.id == id)
    },
    checkField(field) {
      if (Array.isArray(this.unitMYP[field])) {
        return Boolean(this.unitMYP[field].length) ? 'field-check' : null
      } else {
        return Boolean(this.unitMYP[field]) ? 'field-check' : null
      }
    }
  },
  mounted() {
    this.fetchGetUnitMYP(this.$route.params.id);
  },
  computed: {

  },
}
</script>

<style scoped>
@import '@/assets/css/field.css';

.text-block {
  white-space: pre-wrap;
}

.navbar-myp {
  font-size: 0.9em;

}

.kc-recomend {
  color: rgb(6, 134, 27);
  font-weight: bold;
}

.nav-link {
  padding: 0;
  margin: 0;
  font-weight: 400;
}
.myp-group {
  margin: 5px 0;
  font-size: 1.2em;
}

.myp-field {
  margin-left: 20px;
  margin-right: 5px;
  padding: 5px 0;
  position: relative;
}

.myp-field:before {
  content: "";
  position: absolute;
  left: -20px;
  top: 8px;
  float: left;
  width: 15px;
  height: 15px;
  margin-right: 5px;
  background: url('@/assets/img/check-no.png') no-repeat 50% / 100%;
}
.field-check:before {
  background: url('@/assets/img/check-yes.png') no-repeat 50% / 100%;
}

</style>