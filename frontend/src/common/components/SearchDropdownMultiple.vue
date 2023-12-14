<template>
  <div class="d-flex align-items-center flex-wrap">
    <div class="me-2">
      <div class="d-flex flex-wrap" v-if="selectedItems.length">
        <div v-for="item in selectedItems" :key="item.id" class="d-flex me-2 align-items-center">
          <div class="me-2">{{ item[showName] }}</div>
          <i class="bi bi-dash-square dot-menu" @click="removeItem(item)"></i>
        </div>
      </div>
      <div v-else>{{ title }}</div>
    </div>
    <div class="dropdown">
      <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuModule" data-bs-toggle="dropdown"
        aria-expanded="false" data-bs-auto-close="true">Добавить</button>
      <ul class="dropdown-menu pt-0" aria-labelledby="dropdownMenuModule">
        <li class="px-2 pt-2 sticky-top bg-light">
          <input type="text" class="form-control" placeholder="Поиск..." v-model="searchQuery">
          <hr class="dropdown-divider">
        </li>
        <li v-for="(item, index) in filteredList" :key="index" @click="selectItem(item)">
          <a class="dropdown-item" :class="{ 'active': isSelected(item) }" href="javascript:void(0)">{{ item[showName] }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<script setup>
import { ref, computed, watch } from 'vue';

const BASE_NUMBER = 10

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  propItems: {
    type: Array,
    default: () => []
  },
  showName: {
    type: String,
    default: '',
  },
  propName: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: '',
  }
});

const emit = defineEmits(['update:modelValue', 'select']);

const searchQuery = ref('');
const selectedItems = ref([...props.modelValue]);
const showNumber = ref(BASE_NUMBER);

const filteredList = computed(() => {
  showNumber.value = BASE_NUMBER;
  return props.propItems.filter(item =>
    item[props.showName].toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const isSelected = (item) => {
  return selectedItems.value.includes(item);
};

const removeItem = (item) => {
  const index = selectedItems.value.findIndex(selected => selected === item);
  if (index != -1) {
    selectedItems.value.splice(index, 1);
  }
  emit('update:modelValue', selectedItems.value);
  emit('select', { value: selectedItems.value.map(i => i.id), propName: props.propName });
}

const selectItem = (item) => {
  const index = selectedItems.value.findIndex(selected => selected === item);
  if (index === -1) {
    selectedItems.value.push(item);
  } else {
    selectedItems.value.splice(index, 1);
  }
  searchQuery.value = ''
  emit('update:modelValue', selectedItems.value);
  emit('select', { value: selectedItems.value.map(i => i.id), propName: props.propName });
};

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  selectedItems.value = newVal;
});
</script>
  
<style scoped>
.link-show {
  margin-left: 16px;
}

.dropdown-menu {
  max-height: 400px;
  overflow-y: scroll;
}
</style>
  