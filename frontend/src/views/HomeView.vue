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
    <div class="row">
      <div class="col-md card m-2">
        <div class="card-body">
          <div class="my-2">
            <h5>Преподавание</h5>
            <div>
              <ul v-if="teachingLoads.length">
                <li v-for="tl in teachingLoads" :key="tl.id">
                  <b>{{ tl.subject.name }}</b>: <span v-for="group, index in tl.groups" :key="group.id">
                    {{ group.name }}<span v-if="tl.groups.length != index + 1">, </span> класс</span>
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
        </div>
      </div>
      <div class="col-md card m-2">
        <div class="card-body">
          <div class="my-2">
            <h5>Дедлайны педагогов</h5>
            <div>
              <div>Сдача репортов начальной школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты по предметам начальной школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов средней школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты по предметам средней школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов старшей школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты по предметам старшей школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
            </div>
          </div>
          <div class="my-2">
            <h5>Дедлайны службы сопровождения</h5>
            <div>
              <div>Сдача репортов начальной школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты службы сопровождения начальной школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов средней школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты службы сопровождения средней школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов старшей школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты службы сопровождения старшей школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
            </div>
          </div>
          <div class="my-2">
            <h5>Дедлайны классных руководителей</h5>
            <div>
              <div>Сдача репортов начальной школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты классного руководителя начальной школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов средней школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты классного руководителя средней школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
              <div>Сдача репортов старшей школы: <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=Дедлайн сдачи репортов&dates=20231229T120000Z/20231229T120000Z&details=Необходимо написать все репорты классного руководителя старшей школы&sf=true&output=xml" target="_blank">29.12.2023</a></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const teachingLoads = computed(() => {
  return authStore.user.teaching_loads
})



</script>

<style lang="scss" scoped>
.test {
  font-size: 45px;
}
</style>