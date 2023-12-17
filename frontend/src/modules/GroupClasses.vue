<template>
  <div>
    <div class="d-flex flex-wrap">
      <div v-for="groups, year in groupByNestedProperty(propItems, 'year_study', 'number')" :key="year" class="d-flex flex-column align-items-center m-1">
        <!-- <div class="align-center">{{ year }}</div> -->
        <div class="btn-group-vertical" role="group" aria-label="Базовая группа переключателей радио">
          <template v-for="group in groups" :key="group.id">
            <input type="radio" class="btn-check" :value="group" :id="`group-${group.id}`" autocomplete="off" v-model="selectedItem" @change="selectItem(group)">
            <label class="btn btn-outline-secondary" :for="`group-${group.id}`">{{ group.name }}</label>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: {}
  },
  propItems: {
    type: Array,
    default: () => []
  },
});

function groupByNestedProperty(items, key, subKey) {
  return items.reduce((accumulator, item) => {
    // Получаем ключ для группировки из вложенного свойства текущего элемента
    const groupKey = item[key][subKey];

    // Если в аккумуляторе еще нет этой группы, создаем ее
    if (!accumulator[groupKey]) {
      accumulator[groupKey] = [];
    }

    // Добавляем текущий элемент в соответствующую группу
    accumulator[groupKey].push(item);

    return accumulator;
  }, {}); // Начальное значение аккумулятора - пустой объект
}

const emit = defineEmits(['update:modelValue', 'select']);

const selectedItem = ref(props.modelValue || {});

const selectItem = (item) => {
  selectedItem.value = item;
  emit('update:modelValue', selectedItem.value);
  emit('select', { value: selectedItem.value.id, propName: props.propName });
};

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  selectedItem.value = newVal;
});
</script>