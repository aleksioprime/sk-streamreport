<template>
  <div class="col-auto my-1">
    <div class="btn-group">
      <button type="button" class="btn btn-outline-secondary">
        <span v-if="date">
          {{ formatDateToReadable(date) }}
        </span>
        <span v-else>Не выбраны даты</span>
      </button>
      <button class="btn btn-secondary dropdown-toggle dropdown-toggle-split" type="button" data-bs-toggle="dropdown"
        data-bs-auto-close="true" aria-expanded="false">
        <span class="visually-hidden">Toggle Dropdown</span>
      </button>
      <div class="dropdown-menu p-0 border-0 text-body-secondary">
        <div>
          <VDatePicker v-model="date" @dayclick="handleSelect"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { formatToYYYYMMDD, formatDateToReadable } from "@/common/helpers/date.js";

const props = defineProps({
  propDate: [String],
  propName: {
    type: String,
    default: ''
  },
});

// Определяем в emit событие сохранение поля
const emit = defineEmits(['save']);

const date = ref(props.propDate);

// Активируем событие сохранения значения поля
const handleSelect = (date) => {
  console.log('Выбранная дата: ', date.date);
  emit('save', { value: formatToYYYYMMDD(date.date), propName: props.propName });
}

</script>