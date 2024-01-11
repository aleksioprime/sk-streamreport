<template>
  <div class="d-flex">
    <div class="flex-grow-1 test">
      <div v-if="!editMode">
        <div v-if="text" v-html="text" class="custom-style"></div>
        <div v-else>Нет информации</div>
      </div>
      <div v-else class="flex-grow-1">
        <div v-show="tinyLoading">
          <Editor api-key="j30bef5hr2ipfdbu7b9lww7t4oez2v6f27c94otp9to2j9mk" :init="{
            plugins: 'paste lists link wordcount autoresize',
            menubar: false,
            toolbar: 'removeformat | bold italic | forecolor | bullist numlist | link ',
            contextmenu: false,
            paste_as_text: true,
            setup: (ed) => {
              ed.on('init', () => { tinyLoading = true });
            }
          }" model-events="change keydown blur focus" output-format="html" v-model="text"/>
        </div>
        <div v-if="!tinyLoading" class="d-flex align-items-center justify-content-center">
          <span class="loader-line"></span>
        </div>
      </div>
    </div>
    <div v-if="allowedMode" class="border-start ms-2">
      <div v-if="!editMode">
        <button type="button" class="btn btn-link text-muted small" v-if="!isEditing"
          @click="enableEditMode">Изменить</button>
      </div>
      <div v-else class="ms-auto d-flex flex-column align-items-start">
        <button type="button" class="btn btn-link small" @click="submitUpdate">Сохранить</button>
        <button type="button" class="btn btn-link text-muted small" @click="cancelUpdate">Отмена</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import Editor from '@tinymce/tinymce-vue'
import { ref, watch } from 'vue';

const props = defineProps({
  propData: {
    type: String,
    default: ''
  },
  propName: {
    type: String,
    default: ''
  },
  isEditing: {
    type: Boolean,
    default: false,
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

const editMode = ref(false);
const originalText = ref(props.propData);
const text = ref(props.propData);
const tinyLoading = ref(false);

const emit = defineEmits(['save', 'toggleEdit']);

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.propData, (newVal) => {
  text.value = newVal;
  originalText.value = newVal;
});

// Активация режима редактирования
const enableEditMode = () => {
  editMode.value = true;
  emit('toggleEdit', true);
};

// Отмена редактировани
const cancelUpdate = (event) => {
  editMode.value = false;
  text.value = originalText.value;
  emit('toggleEdit', false);
};

// Применение редактирования
const submitUpdate = (event) => {
  editMode.value = false;
  emit('save', { value: text.value, propName: props.propName });
  emit('toggleEdit', false);
};
</script>

<style scoped>
.custom-style p {
  margin-bottom: 0px !important;
  
}
.custom-style {
  overflow-wrap: break-word;
}

.test {
  /* white-space: nowrap; */
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>