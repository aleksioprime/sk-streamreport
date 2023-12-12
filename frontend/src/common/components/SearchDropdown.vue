<template>
  <div>
    <div class="dropdown">
      <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuModule" data-bs-toggle="dropdown"
        aria-expanded="false">
        {{ truncateText(selectedItem[showName], 50) || title }}
      </button>
      <ul class="dropdown-menu pt-0" aria-labelledby="dropdownMenuModule">
        <li class="px-2 pt-2 sticky-top bg-light">
          <input type="text" class="form-control" placeholder="Поиск..." v-model="searchQuery">
          <hr class="dropdown-divider">
        </li>
        <li v-for="(item, index) in filteredList" :key="index" @click="selectItem(item)">
          <a class="dropdown-item" :class="{active: item == selectedItem}" href="##">{{ item[showName] }}</a>
        </li>
        <!-- <li v-if="filteredList.length > showNumber" @click="loadItems">
          <a href='#' class="small text-muted link-show">Показать еще...</a>
        </li> -->
      </ul>
    </div>
  </div>
</template>
  
<script setup>
import { ref, computed, watch } from 'vue';
import { truncateText } from '@/common/helpers/text'
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
  }
});

const emit = defineEmits(['update:modelValue', 'select']);

const searchQuery = ref('');
const selectedItem = ref({});
const showNumber = ref(BASE_NUMBER);

const loadItems = () => {
  // Здесь должен быть код для загрузки данных
  showNumber.value += 3;
};

const filteredList = computed(() => {
  showNumber.value = BASE_NUMBER;
  return props.propItems.filter(item =>
    item[props.showName].toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const selectItem = (item) => {
  selectedItem.value = item;
  searchQuery.value = ''
  showNumber.value = BASE_NUMBER;
  emit('update:modelValue', selectedItem.value);
  emit('select');
};

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  selectedItem.value = newVal;
});
</script>
  
<style scoped>
.link-show {
  margin-left: 16px;
}
.dropdown-menu {
  max-height: 400px;
  max-width: 70vh;
  overflow-y: scroll;
}
</style>
  