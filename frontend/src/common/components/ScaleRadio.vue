<template>
  <div class="btn-group" role="group" aria-label="ScaleRadio">
    <div class="btn-group" role="group" aria-label="ScaleRadio" v-for="item, index in data" :key="item.value">
      <input type="radio" class="btn-check" :name="`radio${elementId}-${index}`" :id="`btnradio${elementId}-${index}`"
        autocomplete="off" v-model="value" :value="item.value" @change="handleSelect" />
      <label class="btn btn-outline-primary custom-label" :for="`btnradio${elementId}-${index}`">{{ item.name }}</label>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  propName: {
    type: String,
    default: ''
  },
  propValue: {
    type: Number,
    default: null
  },
  elementId: {
    type: String,
    default: ''
  }
});

const value = ref(props.propValue);

const emit = defineEmits(['save']);

// Активируем событие сохранения значения поля
const handleSelect = () => {
  emit('save', { value: value.value, propName: props.propName });
}
</script>

<style scoped>
.custom-label {
  padding: 5px 10px;
}
</style>