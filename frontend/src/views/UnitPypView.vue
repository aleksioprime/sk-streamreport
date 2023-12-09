<template>
  <div>
    <h1>Юниты в PYP</h1>
    <div class="py-2">
    </div>
    <div>
      <div v-for="unit in unitPypStore.pypUnits" :key="unit.id">
        <div class="card my-1">
          <div class="card-body">
            {{ unit.title }}
          </div>
        </div>
      </div>
    </div>
    <!-- Подключение модального окна -->
    <confirmation-modal @confirm="removeUnitPypPlanner" @cancel="cancelRemoveUnitPypPlanner">
      Вы действитель хотите удалить репорт студента:
    </confirmation-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";

import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
let confirmationModal = null;

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

const removeUnitPypPlanner = () => {
  // console.log('Запрос на удаление репорта студенту: ', currentStudent.value);
  confirmationModal.hide();
};

const cancelRemoveUnitPypPlanner = () => {
  confirmationModal.hide();
};

onMounted(() => {
  unitPypStore.loadPypUnitPlanners();
  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
});
</script>