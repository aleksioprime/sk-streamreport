<template>
  <div class="d-flex align-items-center">
    <div class="w-100">
      <span v-if="!editMode">{{ text || 'Нет информации' }}</span>
      <input v-else ref="inputRef" type="text" v-model="text" @blur="toggleEditMode" @keyup="handleKeyup"
        class="form-control bottom-border-only">
    </div>
    <div class="me-0 ms-2 text-muted small" v-if="allowedMode">
      <a href="javascript:void(0)" @click.prevent="enableEditMode" v-if="!editMode">Изменить</a>
      <a href="javascript:void(0)" @click.prevent="toggleEditMode" v-else>Отмена</a>
    </div>
    
  </div>
</template>

<script setup>

import { ref, watch, nextTick } from 'vue';

// Определяем пропс и эмит
const props = defineProps({
  modelValue: [String, Number],
  propName: {
    type: String,
    default: ''
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

const emit = defineEmits(['update:modelValue', 'save']);

// Реактивные данные и методы
const editMode = ref(false);
const text = ref(props.modelValue);
const originalText = ref(props.modelValue);
const inputRef = ref(null);

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  text.value = newVal;
  originalText.value = newVal;
});

const toggleEditMode = (event) => {
  if (event.type === 'blur' || (event.type === 'keyup' && event.key === 'Escape')) {
    editMode.value = false;
    text.value = originalText.value; // Возвращаем к исходному значению
  }
};

const handleKeyup = (event) => {
  if (event.key === 'Enter') {
    originalText.value = text.value; // Сохраняем новое значение
    editMode.value = false;
    emit('update:modelValue', text.value);
    emit('save', { value: text.value, propName: props.propName });
  } else if (event.key === 'Escape') {
    text.value = originalText.value; // Возвращаем к исходному значению
    editMode.value = false;
  }
};

// Изменение режима редактирования при клике на span
const enableEditMode = () => {
  editMode.value = true;
  nextTick(() => {
    inputRef.value.focus();
  });
};

</script>

<style scoped>
.bottom-border-only {
  border: none;
  border-bottom: 1px solid #cdcdcd;
  /* Цвет Bootstrap Primary */
  border-radius: 0;
  /* Удалить скругление */
  box-shadow: none;
  /* Удалить тень (если она есть) */
  background-color: transparent;
  /* Прозрачный фон */
  padding-left: 5px;
  padding-top: 0;
}

.bottom-border-only:focus {
  border-bottom: 1px solid #7b7b7b;
  /* Темнее цвет при фокусе */
  box-shadow: none;
  /* Удалить тень при фокусе */
}
</style>