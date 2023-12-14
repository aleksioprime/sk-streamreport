<template>
  <div class="d-flex">
    <div class="w-100">
      <span v-if="!editMode">{{ text || 'Нет информации' }}</span>
      <textarea v-else ref="inputRef" class="form-control bottom-border-only" rows="1" v-model="text" @blur="toggleEditMode" @keydown="handleKeyup"></textarea>
    </div>
    <div class="me-0 ms-2 text-muted small">
      <a href="javascript:void(0)" @click.prevent="enableEditMode" v-if="!editMode">Изменить</a>
      <div v-else>
        <a href="javascript:void(0)" @click.prevent="toggleEditMode" >Отмена</a>
      </div>
    </div>
    
  </div>
</template>

<script setup>

import { ref, watch, nextTick } from 'vue';

// Определяем пропс и эмит
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  propName: {
    type: String,
    default: ''
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
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault(); // Предотвратить перенос текста на новую строку
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
    inputRef.value.addEventListener('input', function () {
      this.style.height = 'auto'; // Сбросить текущую высоту
      this.style.height = this.scrollHeight + 'px'; // Установить новую высоту
    });
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