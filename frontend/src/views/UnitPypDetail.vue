<template>
  <div>
    <h1>PYP: Просмотр и редактирование юнита</h1>
    <div class="row">
      <div class="col-md-3">
        <div class="d-flex flex-column list-menu pt-3 ps-4">
          <a href="#base">Основная информация</a>
          <a href="#central_idea" :class="checkField('central_idea')">Центральная идея</a>
          <a href="#key_concepts" :class="checkField('key_concepts')">Ключевые концепты</a>
          <a href="#related_concepts" :class="checkField('related_concepts')">Сопутствующие концепты</a>
          <a href="#ibprofiles" :class="checkField('ibprofiles')">Качества портрета студента</a>
          <a href="#lines_inquiry" :class="checkField('lines_inquiry')">Линии исследования</a>
          <a href="#atl_develops" :class="checkField('atl_develops')">Навыки ATL</a>
          <a href="#action" :class="checkField('action')">Действия</a>
          <a href="#reflections_initial" :class="checkField('reflections_initial')">Начальная рефлексия</a>
          <a href="#prior_learning" :class="checkField('prior_learning')">Предшествующий опыт</a>
          <a href="#connections" :class="checkField('connections')">Связи: трансдисциплинарные и прошлые</a>
          <a href="#learning_goals" :class="checkField('learning_goals')">Цели обучения и критерии успеха</a>
          <a href="#questions_teacher" :class="checkField('questions_teacher')">Вопросы учителей</a>
          <a href="#questions_student" :class="checkField('questions_student')">Вопросы студентов</a>
          <a href="#engaging_learning" :class="checkField('engaging_learning')">Создание вовлеченного обучения</a>
          <a href="#supporting_agency" :class="checkField('supporting_agency')">Поддержание свободного волеизъявления студентов</a>
          <a href="#questions_all" :class="checkField('questions_all')">Вопросы</a>
          <a href="#ongoing_assessment" :class="checkField('ongoing_assessment')">Текущее оценивание</a>
          <a href="#resources" :class="checkField('resources')">Гибкое использование ресурсов</a>
          <a href="#peer_self_assessment" :class="checkField('peer_self_assessment')">Самооценка учащихся и отзывы сверстников</a>
          <a href="#reflections_ongoing" :class="checkField('reflections_ongoing')">Текущее оценивание</a>
          <a href="#reflections_additional" :class="checkField('reflections_additional')">Дополнительная рефлексия по предметам</a>
          <a href="#reflection_posts" :class="checkField('reflection_posts')">Рефлексия</a>
        </div>
      </div>
      <div class="col pt-3">
        <div v-if="isLoadedUnitPyp">
          <h5 id="base" class="mb-3">Основные данные</h5>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Название юнита: </div>
            <div class="flex-grow-1">
              <editable-text v-model="unitPypStore.pypUnit.title" propName="title"
                @save="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Номер модуля: </div>
            <div class="flex-grow-1">
              <editable-text v-model="unitPypStore.pypUnit.order" propName="order"
                @save="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Учителя: </div>
            <div class="flex-grow-1">
              <search-dropdown-multiple title="Добавить учителя" v-model="unitPypStore.pypUnit.teachers"
                :propItems="generalStore.users" showName="short_name" propName="teachers"
                @select="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Параллель: </div>
            <div class="flex-grow-1">
              <simple-dropdown title="Выберите параллель" v-model="unitPypStore.pypUnit.year"
                :propItems="generalStore.studyYears" showName="name" propName="year"
                @select="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Трансдицсиплинарная тема: </div>
            <div class="flex-grow-1">
              <simple-dropdown title="Выберите тему" v-model="unitPypStore.pypUnit.transdisciplinary_theme"
                :propItems="unitPypStore.transdisciplinaryThemes" showName="name_rus" propName="transdisciplinary_theme"
                @select="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-2 d-flex align-items-center">
            <div class="me-2">Описание: </div>
            <div class="flex-grow-1">
              <editable-area v-model="unitPypStore.pypUnit.description" propName="description"
                @save="handleSave($event, unitPypStore.pypUnit.id)" />
            </div>
          </div>
          <hr>
          <div class="my-3">
            <h5 id="central_idea">Центральная идея</h5>
            <small>
              Инициирует ли центральная идея исследовательский процесс и поддерживает ли концептуальное понимание
              трансдисциплинарной темы студентами
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.central_idea" propName="central_idea"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="key_concepts">Ключевые концепты</h5>
            <small>
              Определяют ли ключевые концепции направление исследования и предоставляют ли возможности для установления
              связей между предметами и за их пределами?
            </small>
            <editable-checkbox v-model="unitPypStore.pypUnit.key_concepts" :propItems="unitPypStore.pypKeyConcepts"
              propName="key_concepts" showName="name_rus" @select="handleSave($event, unitPypStore.pypUnit.id)" />
          </div>
          <div class="my-3">
            <h5 id="related_concepts">Сопутствующие концепции</h5>
            <small>
              Предоставляют ли предметные концепции линзу для концептуального понимания конкретного предмета?
            </small>
            <unit-pyp-related-concept :unit="unitPypStore.pypUnit" />
          </div>
          <div class="my-3">
            <h5 id="ibprofiles">Качества портрета студента</h5>
            <small>
              Какие возможности появятся для развития, демонстрации и усиления качеств портрета студента?
            </small>
            <unit-profile-develop :unit="unitPypStore.pypUnit" />
          </div>
          <div class="my-3">
            <h5 id="lines_inquiry">Линии исследования</h5>
            <small>Какие вопросы учителя и провокации будут формировать линии исследования?<br>
              Линии исследования:
              <ul>
                <li>Проясняют и развивают понимание центральной идеи</li>
                <li>Определить область исследования и помочь сфокусировать обучение и преподавание?</li>
              </ul>
            </small>
            <unit-pyp-lines-of-inquiry :unit="unitPypStore.pypUnit" />
          </div>
          <div class="my-3">
            <h5 id="atl_develops">Подходы к обучению (навыки ATL)</h5>
            <unit-pyp-atl-develop :unit="unitPypStore.pypUnit" />
          </div>
          <div class="my-3">
            <h5 id="action">Действия</h5>
            <small>
              Какие существуют возможности для использования предшествующего обучения для поддержки потенциальных
              действий, инициированных учащимися?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.action" propName="action"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="reflections_initial">Начальная рефлексия</h5>
            <small>
              Как наши первоначальные размышления могут повлиять на все обучение и преподавание в этой теме исследования?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.reflections_initial" propName="reflections_initial"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="prior_learning">Предшествующий опыт</h5>
            <small>
              Как мы оцениваем предыдущие знания, концептуальное понимание и навыки учащихся?
              Как мы используем данные и предыдущий опыт обучения при планировании темы исследования?
              Как в нашем планировании учитывается языковой профиль учащихся?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.prior_learning" propName="prior_learning"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="connections">Связи: трансдисциплинарные и прошлые</h5>
            <small>
              Связи с прошлым и будущим опытом/учением, внутри и вне программы исследования
              Какие существуют связи с обучением внутри и вне темы исследования?
              Какие возможности есть у учащихся для развития концептуального понимания для поддержки передачи опыта между
              предметами и за их пределами?
              Как мы можем гарантировать, что обучение является целенаправленным и связано с местными и глобальными
              проблемами и возможностями?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.connections" propName="connections"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="learning_goals">Цели обучения и критерии успеха</h5>
            <small>
              Что мы хотим, чтобы студенты знали, понимали и умели делать?
              Каким образом учителя и ученики совместно конструируют цели обучения и критерии успеха?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.learning_goals" propName="learning_goals"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="questions_teacher">Вопросы учителей</h5>
            <small>
              Какие вопросы учителя и провокации формируют направления исследования?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.questions_teacher" propName="questions_teacher"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="questions_student">Вопросы студентов</h5>
            <small>
              Какие вопросы студентов, предшествующие знания, существующие теории, опыт и интересы будут влиять на
              направления исследования?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.questions_student" propName="questions_student"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="engaging_learning">Создание вовлеченного обучения</h5>
            <small>
              Какой опыт будет содействовать обучению?<br>
              Для всего обучения это значит:
              <ul>
                <li>Создание вопросов, провокаций и опыта, которыe поддерживают знания и концептуальное понимание</li>
                <li>Создание реальных возможностей для учащихся для разработки и демонстрации подходов к обучению и
                  качеств
                  портрета студента</li>
                <li>Создание гибкости в реагировании на интересы, запросы, развивающиеся теории и действия студентов</li>
                <li>Интеграция языков, для поддержки многоязычия</li>
                <li>Определение возможностей для независимого и совместного обучения, управляемого и поддерживающего
                  обучения, а также расширения обучения</li>
              </ul>
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.engaging_learning" propName="engaging_learning"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="supporting_agency">Поддержание свободного волеизъявления студентов</h5>
            <small>
              Как мы узнаем и поддерживаем свободное волеизъявление студентов в обучении и преподавании?<br>
              Для всего обучения это значит:
              <ul>
                <li>Вовлечение студентов в качестве активных участников и со-конструкторов их обучения</li>
                <li>Развитие у учащихся способности планировать, рефлексировать и оценивать чтобы саморегулироввать и
                  самонастраивать процесс обучения</li>
                <li>Поддержка исследований и действий по инициативе студентов</li>
              </ul>
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.supporting_agency" propName="supporting_agency"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="questions_all">Вопросы</h5>
            <small>
              Какие дополнительные вопросы учителя и провокации из развивающихся теорий студентов?<br>
              Какие вопросы возникают у студентов из развивающихся теорий студентов?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.questions_all" propName="questions_all"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="ongoing_assessment">Текущее оценивание</h5>
            <small>
              Какие доказательства мы собираем о новых знаниях, концептуальном понимании и навыках учащихся?
              Как мы отслеживаем и документируем обучение в соответствии с целями обучения и критериями успеха?
              Как мы используем текущее оценивание для информирования о планировании, а также при создании групп и
              перегруппировке студентов?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.ongoing_assessment" propName="ongoing_assessment"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="resources">Гибкое использование ресурсов</h5>
            <small>
              Как ресурсы повысят ценность и цель обучения?<br>
              Для всего обучения это значит:
              <ul>
                <li>продуманное использование ресурсов как в учебном сообществе, так и за его пределами для улучшения и
                  расширения обучения. Это может включать время, людей, места, технологии, учебные пространства и
                  физические
                  материалы.</li>
              </ul>
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.resources" propName="resources"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="peer_self_assessment">Самооценка учащихся и отзывы сверстников</h5>
            <small>
              Какие есть возможности для студентов получить обратную связь от учителей и сверстников?
              Как учащиеся используют эту обратную связь, чтобы самостоятельно оценивать и корректировать свое обучение?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.peer_self_assessment" propName="peer_self_assessment"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="reflections_ongoing">Текущее оценивание</h5>
            <small>
              Как мы отвечаем на возникающие вопросы, теории, запросы и интересы студентов на протяжении всего
              исследования?
              Как мы поддерживаем возможности для действий по инициативе студентов на протяжении всего исследования?
              Как мы можем гарантировать, что обучение является целенаправленным и достоверным и / или связано с реальными
              проблемами и возможностями?
              Как мы развиваем позитивные отношения между домом, семьей и школой как основу для обучения, здоровья и
              благополучия?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.reflections_ongoing" propName="reflections_ongoing"
                  @save="handleSave($event, unitPypStore.pypUnit.id)" :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="reflections_additional">Дополнительная рефлексия по предметам</h5>
            <small>
              Какие возможности есть у учащихся для установления связи с центральной идеей и линиями исследования или
              программой исследования?
              Какие возможности есть у учащихся для развития знаний, концептуального понимания и навыков для поддержки и
              передачи обучения между предметами и за их пределами?
            </small>
            <div class="card">
              <div class="card-body">
                <editable-area-tiny :propData="unitPypStore.pypUnit.reflections_additional"
                  propName="reflections_additional" @save="handleSave($event, unitPypStore.pypUnit.id)"
                  :isEditing="isEditing" @toggleEdit="toggleEdit" />
              </div>
            </div>
          </div>
          <div class="my-3">
            <h5 id="reflection_posts">Рефлексия</h5>
            <unit-reflection-post :unit="unitPypStore.pypUnit" program="pyp" />
          </div>
        </div>
        <div v-else class="d-flex align-items-center justify-content-center">
          <span class="loader"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from 'vue-router'
import EditableText from "@/common/components/EditableText.vue";
import EditableArea from "@/common/components/EditableArea.vue";
import EditableAreaTiny from "@/common/components/EditableAreaTiny.vue";
import SearchDropdownMultiple from "@/common/components/SearchDropdownMultiple.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import EditableCheckbox from "@/common/components/EditableCheckbox.vue";

import UnitPypRelatedConcept from "@/modules/UnitPypRelatedConcept.vue";
import UnitPypAtlDevelop from "@/modules/UnitPypAtlDevelop.vue";
import UnitProfileDevelop from "@/modules/UnitProfileDevelop.vue";
import UnitPypLinesOfInquiry from "@/modules/UnitPypLinesOfInquiry.vue";
import UnitReflectionPost from "@/modules/UnitReflectionPost.vue";

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

import { useGeneralStore } from "@/stores/general";
const generalStore = useGeneralStore();

import { useIboStore } from "@/stores/ibo";
const iboStore = useIboStore();

const route = useRoute()

const isEditing = ref(false);
const toggleEdit = (state) => {
  isEditing.value = state;
};

const isLoadedUnitPyp = ref(false)

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для юнита с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  unitPypStore.updatePypUnitPlanner(updatingData).then((result) => {
    console.log('Результаты участия в мероприятии успешно обновлены: ', result);
  })
};

onMounted(() => {
  unitPypStore.loadPypUnitPlannerDetail(route.params.id).then(() => {
    isLoadedUnitPyp.value = true;
  });
  generalStore.loadStudyYears();
  generalStore.loadUsers(
    {
      params: {
        groups: 2,
      },
    }
  );
  unitPypStore.loadTransdisciplinaryThemes();
  iboStore.loadAtlCategories();
  unitPypStore.loadPypKeyConcepts();
  iboStore.loadLearnerProfiles();
});

const checkField = (field) => {
  const data = unitPypStore.pypUnit[field]
  if (Array.isArray(data)) {
    return data.length > 0 ? 'check' : null;
  } else if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
    return Object.values(data).some(val => val != null && val !== '') ? 'check' : null;
  } else if (typeof data === 'number') {
    return !isNaN(data) && data !== null ? 'check' : null;
  } else {
    return !!data?.trim() ? 'check' : null;
  }
}
</script>

<style scoped>
.list-menu {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: scroll;
  -ms-overflow-style: none;
  scrollbar-width: none; 
}
.list-menu::-webkit-scrollbar {
  display: none;
}
.list-menu a {
  position: relative;
}
.list-menu a:before {
  content: "";
  left: -20px;
  top: 4px;
  position:absolute;
  float: left;
  width: 15px;
  height: 15px;
  margin-right: 5px;
  background: url('@/assets/img/check-no.png') no-repeat 50% / 100%;
}
.list-menu a.check:before {
  background: url('@/assets/img/check-yes.png') no-repeat 50% / 100%;
}
:target::before {
  content: "";
  display: block;
  height: 90px;
  /* Высота вашей фиксированной шапки */
  margin-top: -90px;
}

:target {
  animation: blink 1s ease-in-out 0s 3;
  /* Анимация будет длиться 1 секунду, повторяться 3 раза */
}

@keyframes blink {

  0%,
  100% {
    color: inherit;
  }

  50% {
    color: rgb(128, 0, 123);
  }

  /* Промежуточный цвет фона для мигания */
}
</style>