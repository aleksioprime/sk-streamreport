<template>
  <nav class="navbar navbar-expand-md bg-light">
    <div class="container">
      <router-link :to="{ name: 'home' }" class="navbar-brand d-flex align-items-center pe-0">
        <div class="logo-header"></div>
        <span>STREAM Report</span>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto" v-if="authStore.isAuthenticated">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Учебные планы
            </a>
            <div class="dropdown-menu">
              <router-link :to="{ name: 'home' }" class="dropdown-item">Юниты PYP</router-link>
              <router-link :to="{ name: 'home' }" class="dropdown-item">Юниты MYP</router-link>
              <router-link :to="{ name: 'home' }" class="dropdown-item">Юниты DP</router-link>
              <router-link :to="{ name: 'home' }" class="dropdown-item">Курсы</router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Репорты
            </a>
            <div class="dropdown-menu">
              <router-link :to="{ name: 'reportTeacher' }" class="dropdown-item">Репорты учителя</router-link>
              <router-link :to="{ name: 'home' }" class="dropdown-item">Репорты наставника</router-link>
              <router-link :to="{ name: 'reportExtra' }" class="dropdown-item">Репорты службы сопровождения</router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Портфолио
            </a>
            <div class="dropdown-menu">
              <router-link :to="{ name: 'home' }" class="dropdown-item">Участие в мероприятиях</router-link>
            </div>
          </li>
        </ul>
        <div class="navbar-text d-flex align-items-center dropdown ms-2" v-if="authStore.isAuthenticated">
          <a class="nav-link" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <div class="navbar-user">
              <img :src='authStore.user.photo ? authStore.user.photo : imageTeacher' alt="" width="35" class="me-2 user-photo rounded-circle">
              <div class="navbar-user-name">
                <div v-if="authStore.user.last_name && authStore.user.first_name">
                  {{ authStore.user.first_name }} {{ authStore.user.last_name }}
                </div>
                <div v-else>{{ authStore.user.email }}</div>
              </div>
            </div>
          </a>
          <div class="dropdown-menu">
            <router-link :to="{ name: 'profile' }" class="dropdown-item">Профиль</router-link>
            <router-link :to="'#'" @click="logout" class="dropdown-item">Выход</router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
  
<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import imageTeacher from '@/assets/img/teacher.svg'

const authStore = useAuthStore();

const router = useRouter();

const logout = async () => {
  await authStore.logout();
  await router.replace({ name: "login" });
};
</script>
  
<style scoped>
.navbar-user {
  display: flex;
  justify-content: flex-end;
  position: relative;
  align-items: center;
  min-width: 130px;
  margin-right: 5px;
}

.navbar-brand {
  cursor: pointer;
  font-family: 'Fira Sans', sans-serif;
}

.user-photo {
  width: 30px;
  height: 30px; 
  object-fit: cover;
}

.navbar-user-name {
  display: flex;
  flex-direction: column;
}

.navbar-user-sync {
  font-size: 0.6em;
  text-transform: uppercase;
  font-weight: 700;
}

.navbar-user-sync:hover {
  color: #674A9E;
  text-decoration: underline;
  cursor: pointer;
}

@media screen and (max-width: 768px) {
  .navbar-user {
    justify-content: flex-start;
  }
}</style>