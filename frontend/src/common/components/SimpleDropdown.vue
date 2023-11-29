<template>
  <div>
    <div class="dropdown">
      <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuModule" data-bs-toggle="dropdown" :disabled="disabled"
        aria-expanded="false">
        {{ selectedItem[showName] || title }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuModule">
        <li v-for="(item, index) in propItems" :key="index" @click="selectItem(item)">
          <a class="dropdown-item" :class="{active: item == selectedItem}" href="#">{{ item[showName] }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<script setup>
import { ref, watch } from 'vue';

const BASE_NUMBER = 10

const props = defineProps({
  modelValue: {
    type: Object,
    default: {}
  },
  propItems: {
    type: Array,
    default: () => []
  },
  showName: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  }
});

const emit = defineEmits(['update:modelValue', 'select']);

const selectedItem = ref({});

const selectItem = (item) => {
  selectedItem.value = item;
  emit('update:modelValue', selectedItem.value);
  emit('select');
};

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  selectedItem.value = newVal;
});
</script>
  
<style scoped>
.dropdown-menu {
  max-height: 400px;
  overflow-y: scroll;
}
.dropdown-toggle::after {
  margin-left: 10px;
}
</style>
  