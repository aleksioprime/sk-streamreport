<template>
  <div>
    <h1><span v-if="authStore.isAuthenticated">{{ authStore.user.first_name }}<span
          v-if="authStore.user.middle_name">&nbsp;{{ authStore.user.middle_name }}</span></span>, добро пожаловать в
      StreamReport!</h1>
    <div class="alert alert-info mt-3" role="alert">
      Внимание! Система находится в режиме тестирования и доработки. Если у вас есть вопросы или замечания по
      функционалу, оставьте, пожалуйста, сообщение <b>Алексею Семочкину</b>
      на почту <a href="mailto:asemochkin@sk.ru">asemochkin@sk.ru</a>, в <a href="https://t.me/aleksioprime"
        target="_blank">Telegram</a> или свяжитесь по номеру телефона <a href="tel:+79169246203">+79169246203</a>.
    </div>
    <div class="alert alert-warning mt-3" role="alert" v-if="isSafari">
      <strong>Предупреждение</strong>: Вы используете браузер <strong>Safari</strong>. Для стабильной работы в системе используйте браузер <strong>Google Chrome</strong>
    </div>
    <div class="row">
      <div class="col-md card m-2">
        <div class="card-body">
          <div class="my-2">
            <h5>Преподавание</h5>
            <div>
              <ul v-if="teachingLoads.length">
                <li v-for="loads, group in groupByNestedProperty(teachingLoads, 'subject', 'name')" :key="group">
                  <b>{{ group }}</b>: <span v-for="load,i in loads" :key="load.id">
                    <span v-for="group, index in load.groups" :key="group.id">
                    {{ group.name }}<span v-if="load.groups.length != index + 1">, </span></span>
                    <span v-if="loads.length != i + 1">, </span>
                  </span> {{ pluralizeRu(loads.length, ['класс', 'классы', 'классы']) }}
                </li>
              </ul>
              <div v-else>
                У вас нет педагогической нагрузки. Для её добавления перейдите в свой <router-link :to="{ name: 'profile' }">профиль</router-link>!
              </div>
            </div>
          </div>
          <div class="my-2">
            <h5>Наставничество</h5>
            <div>
              <div v-if="authStore.user.mentor_classes.length">
                Вы являетесь наставником в
                <strong>
                  <span v-for="group, index in authStore.user.mentor_classes" :key="group.id">{{ group.name }}
                    <span v-if="authStore.user.mentor_classes.length != index + 1">, </span>
                  </span>
                </strong>
                классе
              </div>
              <div v-else>
                Вы не являетесь наставником
              </div>
            </div>
          </div>
          <div class="my-2">
            <h5>Сопровождение</h5>
            <div>
              <div v-if="authStore.user.group_roles.length">
                Вы связаны с классами следующими ролями:
                <ul>
                  <li v-for="gr in authStore.user.group_roles" :key="gr.id">
                    <div><b>{{ gr.group.name }}</b>: {{ gr.role }}</div>
                  </li>
                </ul>
              </div>
              <div v-else>
                Вы не связаны со службой сопровождения
              </div>
            </div>
          </div>
          <div class="my-2">
            <h5>Репорты</h5>
            <div class="mb-2">
              Всего мной создано: <b>{{ authStore.user.my_reports_count }}</b> {{ pluralizeRu(authStore.user.my_reports_count, ['репорт', 'репорта', 'репортов']) }}
            </div>
            <div>
              Всего учителями создано: <b>{{ authStore.user.all_teacherreports_count }}</b> {{ pluralizeRu(authStore.user.all_teacherreports_count, ['репорт', 'репорта', 'репортов']) }}
            </div>
            <div>
              Всего службой сопровождения создано: <b>{{ authStore.user.all_extrareports_count }}</b> {{ pluralizeRu(authStore.user.all_extrareports_count, ['репорт', 'репорта', 'репортов']) }}
            </div>
            <div>
              Всего наставниками создано: <b>{{ authStore.user.all_mentorreports_count }}</b> {{ pluralizeRu(authStore.user.all_mentorreports_count, ['репорт', 'репорта', 'репортов']) }}
            </div>
          </div>
        </div>
      </div>
      <div class="col-md card m-2">
        <div class="card-body">
          <div class="my-2">
            <h5>Дедлайны заполнения репортов</h5>
            <div>Общий дедлайн: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты по предметам начальной школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
          </div>
          <div class="my-2">
            <h5>Изменения версии от 27.12.2023:</h5>
            <div>
              <ul>
                <li>Исправлена ошибка автоматической коррекции текста плагинами онлайн-перевода</li>
                <li>Добавлена возможность редактирования репортов в начальной школе и юнитов PYP воспитателями 1-4 классов</li>
                <li>Изменена шкала итоговой оценки в средней и старшей школе</li>
                <li>Скорректированы темы учебных предметов начальной школы</li>
                <li>Исправлено контекстное меню области ввода форматированного текста и добавлена кнопка сброса формата</li>
                <li>Добавлена возможность предоставления персонального доступа для редактирования критериев</li>
                <li>Исправлено поведение всплывающих сообщений</li>
                <li>Скорректированы названия разделов в юнитах PYP</li>
                <li>Исправлены шаблоны репортов начальной школы для выгрузки в Word</li>
                <li>Добавлены англоязычные версии критериев в старшей школе</li>
                <li>Добавлена возможность редактирования репорта учителя, ведущего занятия в другой подгруппе текущего класса</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { pluralizeRu } from '@/common/helpers/text'

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const teachingLoads = computed(() => {
  return authStore.user.teaching_loads
})

const isSafari = computed(() => {
  const userAgent = navigator.userAgent;
  return /Safari/.test(userAgent) && !/Chrome/.test(userAgent);
})

function groupByNestedProperty(items, key, subKey) {
  return items.reduce((accumulator, item) => {
    // Получаем ключ для группировки из вложенного свойства текущего элемента
    const groupKey = item[key][subKey];

    // Если в аккумуляторе еще нет этой группы, создаем ее
    if (!accumulator[groupKey]) {
      accumulator[groupKey] = [];
    }

    // Добавляем текущий элемент в соответствующую группу
    accumulator[groupKey].push(item);

    return accumulator;
  }, {}); // Начальное значение аккумулятора - пустой объект
}

</script>

<style lang="scss" scoped>
.test {
  font-size: 45px;
}
</style>