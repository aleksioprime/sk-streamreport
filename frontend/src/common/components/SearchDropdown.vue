<template>
  <div>
    <div class="dropdown">
      <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuModule" data-bs-toggle="dropdown"
        aria-expanded="false">
        {{ selectedItem[showName] || title }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuModule">
        <li class="mx-2">
          <input type="text" class="form-control" placeholder="Поиск..." v-model="searchQuery">
        </li>
        <li>
          <hr class="dropdown-divider">
        </li>
        <li v-for="(item, index) in filteredList" :key="index" @click="selectItem(item)">
          <a class="dropdown-item" :class="{active: item == selectedItem}" href="#">{{ item[showName] }}</a>
        </li>
        <!-- <li v-if="filteredList.length > showNumber" @click="loadItems">
          <a href='#' class="small text-muted link-show">Показать еще...</a>
        </li> -->
      </ul>
    </div>
  </div>
</template>
  
<script setup>
import { ref, computed } from 'vue';

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

const emit = defineEmits(['update:modelValue', 'save']);

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
  showNumber.value = BASE_NUMBER;
  emit('update:modelValue', selectedItem.value);
};
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
  