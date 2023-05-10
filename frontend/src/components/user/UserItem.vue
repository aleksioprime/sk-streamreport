<template>
  <div class="d-flex py-1 px-1 user-item" @click="$emit('select', user)">
    <div class="user-photo me-3">
      <img :src='user.photo ? user.photo : require("@/assets/img/user.png")' alt="" width="50">
      <div v-if="user.teacher && user.teacher.admin" class="icon-admin"></div>
    </div>
    <div class="d-flex flex-column">
      <div class="user-name">{{ user.last_name }} {{ user.first_name }} {{ user.middle_name }}</div>
      <div>Пользователь: {{ user.username }} ({{ user.email }})</div>
      <div v-if="user.teacher">{{ user.teacher.position }}</div>
    </div>
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
    getGroupStudent(groups) {
      return groups.find(item => item.study_year == 1) || {}
    }
  }
}
</script>

<style>
.user-item {
  cursor: pointer;
}
.user-item:hover {
  background-color: azure;
}
.user-name {
  text-transform: uppercase;
  font-weight: bold;
  color: rgb(61, 62, 63);
}
.user-photo {
  position: relative;
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