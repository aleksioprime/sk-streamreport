<template>
  <div class="user-item" @click="$emit('select', user)">
    <div>{{ user.last_name }} {{ user.first_name }}</div>
    <button class="ms-auto btn-icon img-append" @click="$emit('append', user)"></button>
  </div>
</template>

<script>
export default {
  props: {
    user: {
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

<style scoped>
.user-item {
  display: flex;
  align-items: center;
  padding: 5px 10px;
}
.user-item:hover {
  background-color: azure;
}
.btn-icon {
  border: none;
  width: 20px;
  height: 20px;
  cursor: pointer;
}
.btn-icon:hover {
  transform: scale(1.1);
}
.img-append {
  background: url('@/assets/img/item-add.png') no-repeat 50% / 90%;
}
</style>