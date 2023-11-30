<template>
  <div class="d-flex align-items-center wrapper">
    <div v-if="!editMode" class="cell-text" @click="enableEditMode">{{ text || "Нажмите, чтобы написать комментарий" }}
    </div>
    <textarea v-else id="cell-input" ref="inputRef" type="text" v-model="text" @blur="toggleEditMode" @keydown="handleKeyup"
      class="form-control"></textarea>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

// Определяем пропс и эмит
const props = defineProps({
  propData: {
    type: String,
    default: ''
  },
  propName: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['save']);

// Реактивные данные и методы
const editMode = ref(false);
const text = ref(props.propData);
const originalText = ref(props.propData);
const inputRef = ref(null);

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
.wrapper {
  max-height: 100vh;
  width: 100%;
}

.cell-text {
  cursor: pointer;
  font-size: 0.9rem;
}

#cell-input {
  border: none;
  box-shadow: none;
  resize: none;
  padding: 5px;
}
</style>