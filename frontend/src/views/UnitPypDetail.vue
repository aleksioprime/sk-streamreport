<template>
  <div>
    <h1>PYP: Просмотр и редактирование юнита</h1>
    <div>{{ unitPypStore.pypUnit }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from 'vue-router'

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

const route = useRoute()

onMounted(() => {
  unitPypStore.loadPypUnitPlannerDetail(route.params.id);
});
</script>