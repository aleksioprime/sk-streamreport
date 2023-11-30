<template>
  <app-layout-default>
    <div v-if="authStore.alertSuccess" :class="authStore.animationClass" class="alert alert-success">
      Данные успешно сохранены!
    </div>
    <router-view v-if="isLoaded" />
  </app-layout-default>
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
.alert {
  position: fixed;
  top: 20px;
  width: calc(90vw);
  z-index: 1;
  /* Дополнительные стили для всплывающего сообщения */
}
</style>
