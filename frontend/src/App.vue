<template>
  <div>
    <!-- TODO: Настроить всплывающие сообщения -->
    <div v-show="authStore.alertSuccess" class="alert alert-success animate__animated block" :class="authStore.animationClass">
      {{ authStore.alertSuccessMessage }}
    </div>
    <!-- TODO: Настроить шаблонизатор -->
    <!-- <app-layout v-if="isLoaded">
      <router-view />
    </app-layout> -->
    <template v-if="isLoaded">
      <app-layout-default v-if="authStore.user">
        <router-view />
      </app-layout-default>
      <div v-else>
        <router-view />
      </div>
    </template>
    
  </div>
</template>

<script setup>
import AppLayout from "@/layouts/AppLayout.vue";
import AppLayoutDefault from "@/layouts/DefaultLayout.vue";
import { onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import JwtService from "@/services/jwt/jwt.service";
import router from "./router";
import { useRoute } from "vue-router";

const route = useRoute();
const isLoaded = ref(false);
const authStore = useAuthStore();

const checkLoggedIn = async () => {
  const token = JwtService.getAccessToken();

  if (!token) {
    isLoaded.value = true;
    return;
  }

  try {
    await authStore.whoami();
    const { redirect } = route.query;
    await router.push(redirect ? redirect : { name: "home" });
  } catch (e) {
    JwtService.destroyTokens();
    console.error(e);
  } finally {
    isLoaded.value = true;
  }
};

onMounted(() => {
  checkLoggedIn();
});
</script>

<style scoped>
.block {
  position: fixed;
  top: 10px;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 1;
  text-align: center;
  /* Дополнительные стили для всплывающего сообщения */
}
</style>
