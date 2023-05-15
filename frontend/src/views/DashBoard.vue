<template>
  <div>
    <base-header>
      <template v-slot:header>Информационная панель</template>
    </base-header>
    <div class="area p-3">
      <h4>Доброго времени суток, {{ authUser.first_name }}!</h4>
      <div class="my-3">Вы находитесь в экспериментальной системе <b>Stream Report</b> Международной Гимназии Сколково</div>
      <div><b>Stream Report</b> в настоящий момент находится в разработке, но некоторые функции уже доступны.</div>
      <div class="mt-5">Если вы нашли ошибки, неработающие фукнции, то сообщите разработчику по адресу <b>asemochkin@sk.ru</b></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'DashBoard',
  data() {
    return {

    }
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
}
</script>

<style></style>