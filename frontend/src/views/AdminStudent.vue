<template>
  <div>
    <base-header>
      <template v-slot:header>Cписок студентов</template>
    </base-header>
    <!-- Кнопки добавления, редактирования, удаления пользователей -->
    <div class="btn-wrapper sticky-top">
      <button class="btn btn-primary my-3" @click="showAddUser">Добавить студента</button>
      <button class="btn-icon img-import ms-2" type="button" @click="showImportUser"></button>
      <div v-if="currentUser.id && !flagUser.add" class="my-3 d-flex align-items-center ms-auto">
        <button type="button" class="btn-icon img-photo ms-2" @click="showEditPhoto"></button>
        <button type="button" class="btn-icon img-pass ms-2" @click="showEditPass"></button>
        <button type="button" class="btn-icon img-edit ms-4" @click="showEditUser"></button>
        <button type="button" class="btn-icon img-del ms-2" @click="showDelUser"></button>
        <!-- <button type="button" class="btn btn-primary ms-4" @click="showEditUser">Редактировать</button>
        <button type="button" class="btn btn-primary ms-2" @click="showDelUser">Удалить</button> -->
      </div>
    </div>
    <!-- Инструменты фильтрации студентов -->
    <filter-student @searchUser="userSearch" v-model:currentYear="currentYear" />
    <!-- Список студентов -->
    <div v-if="!isUserLoading" class="mt-3">
      <div>Всего студентов: <b>{{ totalUsers }}</b></div>
      <user-list :users="users"  @changePage="changePage" v-model:currentUser="currentUser" :currentYear="currentYear"
        :totalPages="totalPages" :currentPage="currentPage" :flagUser="flagUser"/>
    </div>
    <div v-else class="loader">
      <div class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <!-- Модальное окно добавления/редактирования/удаления пользователя -->
    <modal-user :modalTitle="modalTitle" @cancel="hideUserModal" :flagUser="flagUser"
      @create="userCreate" @update="userUpdate" @delete="userDelete" @import="userImport">
      <template v-slot:body>
        <form-student ref="formStudent" v-if="flagUser.add || flagUser.edit" :addMode="flagUser.add"
          v-model:editedUser="editedUser" v-model:validFormStudent="validFormStudent" :currentYear="currentYear"/>
        <form-import v-if="flagUser.import" v-model="newUsers" />
        <div v-if="flagUser.delete">
          <div>Вы действительно хотите удалить этого студента?</div>
          <div class="user-delete">
            <div>{{ editedUser.last_name }} {{ editedUser.first_name }} {{ editedUser.middle_name }}</div>
            <div>Логин: {{ editedUser.username }}</div>
            <div>E-mail: {{ editedUser.email }}</div>
          </div>
        </div>
      </template>
    </modal-user>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { getUsers, createUser, updateUser, deleteUser } from "@/hooks/user/useUser";
import { getGroups } from "@/hooks/user/useGroup";
import FormImport from "@/components/user/FormImport";
import UserList from "@/components/user/UserList";
import FilterStudent from "@/components/user/FilterStudent";
import FormStudent from "@/components/user/FormStudent";
export default {
  name: 'StudentBoard',
  components: {
    UserList, FilterStudent, FormStudent, FormImport
  },
  setup(props) {
    const { users, isUserLoading, totalPages, totalUsers, fetchGetUsers } = getUsers();
    const { groups, fetchGetGroups } = getGroups();
    const { fetchCreateUser } = createUser();
    const { fetchUpdateUser } = updateUser();
    const { fetchDeleteUser } = deleteUser();
    return {
      users, isUserLoading, totalPages, totalUsers, fetchGetUsers,
      fetchCreateUser, fetchUpdateUser, fetchDeleteUser,
      groups, fetchGetGroups,
    }
  },
  data() {
    return {
      currentPage: 1,
      limit: 15,
      currentUser: {},
      editedUser: {},
      flagUser: {},
      modalTitle: '',
      validFormStudent: false,
      searchValue: null,
      currentYear: null,
      newUsers: [],
    }
  },
  methods: {
    // Выбор текущей страницы
    changePage(page) {
      this.currentPage = page;
      this.fetchGetUsers({ role: "student", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    // Открытие модального окна для добавления студента 
    showAddUser() {
      this.modalTitle = "Добавление студента";
      this.flagUser.add = true;
      this.editedUser = {
        gender: 'O',
        student: {}
      };
      this.modalUser.show();
    },
    // Открытие модального окна для редактирования студента 
    showEditUser() {
      this.modalTitle = "Редактирование студента";
      this.editedUser = { ...this.currentUser }
      this.editedUser.student = { ...this.currentUser.student }
      console.log(this.editedUser)
      this.flagUser.edit = true;
      this.modalUser.show();
    },
    // Открытие модального окна для удаления студента 
    showDelUser() {
      this.modalTitle = "Удаление студента";
      this.editedUser = { ...this.currentUser }
      this.flagUser.delete = true;
      this.modalUser.show();
    },
    // Открытие модального окна для импорта студентов
    showImportUser() {
      this.modalTitle = 'Импорт студентов';
      this.flagUser.import = true;
      this.modalUser.show();
    },
    // Закрытие модального окна
    hideUserModal() {
      this.validFormStudent = false;
      this.editedUser = {};
      this.modalUser.hide();
      this.flagUser = {};
    },
    // Валидация формы и отправка запроса на добавления сотрудника
    userCreate() {
      this.$refs.formStudent.checkFieldsValidate();
      if (this.validFormStudent) {
        console.log("Запрос на создание пользователя: ", this.editedUser);
        this.fetchCreateUser(this.editedUser).then(() => {
          this.hideUserModal();
          this.fetchGetUsers({ role: "student", page: this.currentPage, limit: this.limit });
        })
      } else {
        console.log('Валидация неуспешна', this.currentUser)
      }
    },
    // Валидация формы и отправка запроса на обновление информации о сотруднике
    userUpdate() {
      this.$refs.formStudent.checkFieldsValidate();
      if (this.validFormStudent) {
        delete this.editedUser.teacher;
        console.log("Запрос на обновление пользователя: ", this.editedUser);
        this.fetchUpdateUser(this.editedUser).then(() => {
          this.hideUserModal();
          this.fetchGetUsers({ role: "student", page: this.currentPage, limit: this.limit });
        });
      } else {
        console.log('Валидация неуспешна', this.currentUser)
      }
    },
    // Валидация формы и отправка запроса на удаление сотруднике
    userDelete() {
      this.fetchDeleteUser(this.editedUser).then(() => {
        this.hideUserModal();
        this.fetchGetUsers({ role: "student", page: this.currentPage, limit: this.limit });
      });
    },
    // 
    userImport() {
      const data = {
        'users_import': this.newUsers,
        'users_role': 'student',
      }
      this.axios.post('/user/import', data)
        .then((response) => {
          console.log(response);
          this.users = response.data;
          this.currentUser = {};
          this.userCancel();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Поиск студента по фамилии
    userSearch(search) {
      this.currentPage = 1;
      this.searchValue = search;
      this.fetchGetUsers({ role: "student", search: search, limit: this.limit });
    }
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalUser = new Modal('#modalUser', { backdrop: 'static' });
    // Запросы данных при загрузке страницы
    this.fetchGetUsers({ role: "student", page: this.currentPage, limit: this.limit });
  },
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.btn-icon {
  border: none;
  width: 20px;
  height: 20px;
  cursor: pointer;
}
.btn-icon:hover {
  transform: scale(1.2);
}
.img-delete {
  background: url('@/assets/img/item-delete.png') no-repeat 50% / 90%;
}
.img-import {
  background: url('@/assets/img/item-import.png') no-repeat 50% / 90%;
}
</style>