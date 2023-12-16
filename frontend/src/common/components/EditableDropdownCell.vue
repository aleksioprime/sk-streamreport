<template>
  <div class="d-flex align-items-center wrapper">
    <simple-dropdown :title="title" v-model="value" :propItems="propItems" :showName="showName" @select="handleSelect" :disabled="disabled"/>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";

// Определяем в props текущее значение поля и название этого поля
const props = defineProps({
  propData: [String, Object],
  propName: {
    type: String,
    default: ''
  },
  propItems: {
    type: Array,
    default: () => []
  },
  showName: {
    type: String,
    default: '',
  },
  saveName: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    default: '-',
  },
  disabled: {
    type: Boolean,
    default: false,
  }
});

// Определяем в emit событие сохранение поля
const emit = defineEmits(['save']);

// Реактивные данные: значение поля находим в полученном списке, из которого будем выбирать
const value = ref(props.propItems.find((item) => {
  if (props.propData instanceof Object) {
    // console.log(item[props.saveName], props.propData[props.saveName])
    return item[props.saveName] == props.propData[props.saveName]
  } else {
    return item[props.saveName] == props.propData
  }
}));
const originalValue = ref(props.propData);

// Активируем событие сохранения значения поля
const handleSelect = () => {
  originalValue.value = value.value; // Сохраняем новое значение
  emit('save', { value: value.value[props.saveName], propName: props.propName });
}

</script>

<style scoped>
.wrapper {
  max-height: 100vh;
  width: 100%;
}
</style>