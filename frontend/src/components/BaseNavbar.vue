<template>
  <nav class="navbar navbar-expand-md bg-light">
    <div class="container">
      <div @click="$router.push('/')" class="navbar-brand d-flex align-items-center pe-0">
        <img src="@/assets/img/logo.png" alt="" height="35" class="logo-rotate">
        <span>STREAM Report</span>
      </div>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item dropdown" v-if="isAdmin">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Модерация
            </a>
            <div class="dropdown-menu">
              <router-link to="/employee" class="dropdown-item">Сотрудники</router-link>
              <router-link to="/student" class="dropdown-item">Студенты</router-link>
              <router-link to="/group" class="dropdown-item">Учебные классы</router-link>
              <router-link to="/syllabus" class="dropdown-item">Учебные планы</router-link>
              <router-link to="/load" class="dropdown-item">Нагрузка</router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Юниты
            </a>
            <div class="dropdown-menu">
              <router-link to="/myp" class="dropdown-item">Средняя школа</router-link>
              <router-link to="/dp" class="dropdown-item">Старшая школа</router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Оценивание
            </a>
            <div class="dropdown-menu">
              <router-link to="/assessment" class="dropdown-item">Итоговые работы</router-link>
              <router-link to="/schedule" class="dropdown-item">График работ</router-link>
              <router-link to="/report/teacher" class="dropdown-item">Репорты учителя</router-link>
              <router-link to="/report/mentor" class="dropdown-item">Репорты наставника</router-link>
            </div>
          </li>
          <!-- <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Дополнительно
            </a>
            <div class="dropdown-menu">
              <router-link to="/extra/contest" class="dropdown-item">Олимпиады и конкурсы</router-link>
              <router-link to="/extra/teaching" class="dropdown-item">Педагогическое менторство</router-link>
            </div>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/unit" class="nav-link" aria-current="page">Юниты</router-link>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/assessment" class="nav-link">Оценки</router-link>
          </li> -->
          <!-- <li class="nav-item">
            <router-link to="/report" class="nav-link">Репорты</router-link>
          </li> -->
        </ul>
        <div class="navbar-text d-flex align-items-center" v-if="authUser">
          <div class="navbar-user">
            <img :src='authUser.photo ? authUser.photo : require("@/assets/img/user.png")' alt="" width="30" class="me-2">
            <span v-if="authUser.last_name && authUser.first_name">
              {{ authUser.first_name }} {{ authUser.last_name.slice(0, 1) }}.
            </span>
            <span v-else>{{ authUser.username }}</span>
          </div>
          <button class="btn-logout" @click="logout"></button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'BaseNavbar',
  data() {
    return {
    };
  },
  methods: {
    logout() {
      this.$store.dispatch('userLogout').then(() => {
        this.$router.push({ name: 'login' })
      });
    },
  },
  mounted() {
  },
  computed: {
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>

<style>
.pointer {
  cursor: pointer;
}

.logo-rotate {
  display: inline-block;
  margin-right: 10px;
  overflow: hidden;
  -webkit-transition: all 0.5s ease;
  transition: all 0.5s ease;
}

.logo-rotate:hover {
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}
.navbar-user {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  min-width: 130px;
}
.btn-logout {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
  margin-left: 10px;
  background: url('@/assets/img/logout.svg') no-repeat 50% / 90%;
}

@media screen and (max-width: 768px) {
  .navbar-user {
    justify-content: flex-start;
  }
}
</style>