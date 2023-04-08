<template>
  <div v-if="users.length > 0" ref="userlist">
    <div>Всего сотрудников: <b>{{ users.length }}</b></div>
    <transition-group name="user-list">
      <user-item v-for="user in users" :key="user.id" :user="user" @select="selectUser"
        :class="[currentUser == user ? 'select-user' : '']" class="border my-1" />
    </transition-group>
    <nav aria-label="pagination" class="mt-3">
      <ul class="pagination">
        <li class="page-item">
          <a class="page-link" href="#" aria-label="prev" @click="currentPage--">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="page-item" v-for="pageNumber in totalPages" :key="pageNumber"
          :class="{ 'active': currentPage == pageNumber }">
          <a class="page-link" href="#" @click="changePage(pageNumber)">{{ pageNumber }}</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#" aria-label="next" @click="currentPage++">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
  <div v-else>
    Список пользователей пуст
  </div>
</template>

<script>
import UserItem from "@/components/UserItem";
export default {
  name: 'UserList',
  components: {
    UserItem
  },
  props: {
    users: {
      type: Array,
      required: true,
      default: [],
    }
  },
  data() {
    return {
      currentUser: {},
    }
  },
  methods: {
    // Выбор текущего пользователя при нажатии на строку списка
    selectUser(user) {
      if (this.currentUser != user) {
        this.currentUser = user;
      } else {
        this.currentUser = {};
      }
    },
  }
}
</script>

<style></style>