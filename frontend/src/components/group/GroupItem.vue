<template>
  <div class="d-flex py-1 px-1 group-item" @click="$emit('select', group)">
    {{ group.class_year }}{{ group.letter }} класс
  </div>
</template>

<script>
export default {
  props: {
    group: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      
    }
  },
  methods: {
    
  }
}
</script>

<style>
.group-item {
  cursor: pointer;
}
.group-item:hover {
  background-color: azure;
}
.icon-admin {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  background: red;
}
</style>