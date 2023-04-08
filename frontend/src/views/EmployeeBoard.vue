<template>
  <div>
    <base-header>
      <template v-slot:header>Cписок сотрудников</template>
    </base-header>
    <user-list :users="users" />
    <!-- Модальное окно добавления/редактирования/удаления пользователя -->
    <modal-user :modalTitle="modalTitle">
      <template v-slot:body>
        
      </template>
    </modal-user>
  </div>
</template>

<script>
import UserList from "@/components/UserList";
import { getUsers, getRoles, getGroups } from "@/hooks/user/getUserData";
import { Modal } from 'bootstrap';

export default {
  name: 'EmployeeBoard',
  components: {
    UserList
  },
  setup(props) {
    const { users, getUserData } = getUsers()
    return {
      users, getUserData,
    }
  },
  data() {
    return {

    }
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalUser = new Modal('#modalUser', { backdrop: 'static' });
    // Запросы данных при загрузке страницы
    this.getUserData({role: "2,3"});
  },
}
</script>

<style></style>