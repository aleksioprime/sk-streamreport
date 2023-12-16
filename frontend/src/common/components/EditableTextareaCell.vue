<template>
  <div class="d-flex align-items-center wrapper">
    <div v-if="allowedMode">
      <div v-if="!editMode" class="cell-text" @click="enableEditMode">{{ text || "Нажмите, чтобы написать комментарий" }}
      </div>
      <textarea v-else id="cell-input" ref="inputRef" type="text" v-model="text" @blur="toggleEditMode" @keydown="handleKeyup"
        class="form-control"></textarea>
    </div>
    <div v-else>
      {{ text }}
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

// Определяем в props текущее значение поля и название этого поля
const props = defineProps({
  propData: {
    type: String,
    default: ''
  },
  propName: {
    type: String,
    default: ''
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

// Определяем в emit событие сохранение поля
const emit = defineEmits(['save']);

// Реактивные данные и методы
const editMode = ref(false);
const text = ref(props.propData);
const originalText = ref(props.propData);
const inputRef = ref(null);

// Переход в режим редактирования, перевод курсора в поле ввода и привязка функции автоматического увеличения textarea
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

// Отмена редактирования и возврат к предыдущему значению при потере фокуса или нажатия Escape 
const toggleEditMode = (event) => {
  if (event.type === 'blur' || (event.type === 'keyup' && event.key === 'Escape')) {
    editMode.value = false;
    text.value = originalText.value; // Возвращаем к исходному значению
  }
};

// Сохранение результата при нажатии на enter и отмена сохранения при нажатии на Escape
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
</script>

<style scoped>
.wrapper {
  max-height: 100vh;
  width: 100%;
}

.cell-text {
  cursor: pointer;
  font-size: 0.9rem;
  width: 100%;
  height: 100%;
}

#cell-input {
  border: none;
  box-shadow: none;
  resize: none;
  padding: 5px;
}
</style>