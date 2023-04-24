<template>
  <div class="group-item" @click="$emit('select', group)">
    <div>{{ group.class_year }}{{ group.letter }} класс</div>
    <div class="btn-wrapper" v-if="showEditButton">
      <button class="btn-icon img-edit" @click="$emit('update', group)"></button>
      <button class="btn-icon img-delete" @click="$emit('delete', group)"></button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    group: {
      type: Object,
      required: true,
    },
    showEditButton: {
      type: Boolean,
      default: false,
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
  display: flex;
  align-items: center;
  padding: 5px;
}
.group-item:hover {
  background-color: azure;
}
.btn-wrapper {
  margin-left: auto;
  display: flex;
  align-items: center;
}
.btn-icon {
  border: none;
  width: 20px;
  height: 20px;
  cursor: pointer;
}
.btn-icon:not(:last-of-type) {
  margin-right: 5px;
}
.btn-icon:hover {
  transform: scale(1.1);
}
.img-edit {
  background: url('@/assets/img/item-edit.png') no-repeat 50% / 90%;
}
.img-delete {
  background: url('@/assets/img/item-delete.png') no-repeat 50% / 90%;
}
</style>