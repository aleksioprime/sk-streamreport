<template>
  <div>
    <div v-for="item, index in propItems" :key="index" class="form-check">
      <input class="form-check-input" type="checkbox" v-model="selectedItems" 
      :value="item" :id="`item-${propName}-${index}`" @change="selectItem(item)">
      <label class="form-check-label" :class="{'active': isSelected(item)}" :for="`item-${propName}-${index}`">
        {{ item[showName] }}
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: []
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
});

const selectedItems = ref([...props.modelValue]);

const emit = defineEmits(['update:modelValue', 'select']);

const selectItem = (item) => {
  emit('update:modelValue', selectedItems.value);
  emit('select', { value: selectedItems.value.map(i => i.id), propName: props.propName });
};

const isSelected = (item) => {
  return selectedItems.value.map(i => i.id).includes(item.id);
};

// Следим за изменениями modelValue, чтобы обновлять локальное состояние
watch(() => props.modelValue, (newVal) => {
  selectedItems.value = newVal;
});

</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>