<template>
  <div>
    <base-header>
      <template v-slot:header>Учебные группы</template>
    </base-header>
    <!-- Выбор учебного года -->
    <div class="my-2">
      <select id="study-year" class="form-select me-3 mb-2" v-model="currentYear">
        <option v-for="(study, i) in studyYears" :key="i" :value="study">
          {{ study.name }} учебный год
        </option>
      </select>
    </div>
    <!-- Список групп и студентов в них -->
    <div class="row" v-if="!isGroupLoading">
      <div class="col-sm-4">
        <div v-if="groups.length > 0" ref="grouplist" class="accordion" id="accordionGroups">
          <!-- Список групп -->
          <div v-for="(groupsByYear, year) in groupedArrayData(groups, ['class_year'])" :key="year"
            class="accordion-item">
            <h2 class="accordion-header" :id="`heading-${year}`">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                :data-bs-target="`#collapse-${year}`" aria-expanded="false" :aria-controls="`collapse-${year}`">
                {{ year }} классы
              </button>
            </h2>
            <div :id="`collapse-${year}`" class="accordion-collapse collapse" :aria-labelledby="`heading-${year}`"
              data-bs-parent="#accordionGroups">
              <div class="p-1">
                <div v-for="group in groupsByYear" :key="group.id" class="border my-1">
                  <group-item :group="group" @select="groupSelect" @update="showUpdateGroup" @delete="showDeleteGroup"
                    :class="[currentGroup && currentGroup.id == group.id ? 'select-group' : '']" :showEditButton="currentGroup && currentGroup.id == group.id"/>
                  <div v-if="editingGroupID == group.id" class="m-1">
                    <input v-model="editingGroup.class_year" type="number" placeholder="Номер" class="form-control my-1">
                    <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
                    <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
                    <div class="d-flex justify-content-end">
                      <button class="btn-icon img-apply mx-1" @click="groupEdit"></button>
                      <button class="btn-icon img-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                  <div v-else-if="deletingGroupID == group.id" class="m-1">
                    <div>Вы действительно хотите удалить этот класс?</div>
                    <div class="d-flex justify-content-end">
                      <button class="btn-icon img-apply mx-1" @click="groupDelete"></button>
                      <button class="btn-icon img-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                </div>
                <div>
                  <button class="btn-icon img-append" @click="showAddGroup(year)"></button>
                  <div v-if="addingGroupYear == year" class="m-1">
                    <input v-model="editingGroup.class_year" type="number" placeholder="Номер" class="form-control my-1">
                    <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
                    <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
                    <div class="d-flex justify-content-end">
                      <button class="btn-icon img-apply mx-1" :disabled="!(editingGroup.class_year && editingGroup.letter)" @click="groupAdd"></button>
                      <button class="btn-icon img-cancel" @click="groupCancel"></button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button class="btn btn-success btn-sm m-1" @click="showAddGroup(year)">Создать группу</button>
          <div v-if="addingGroupYear == 0" class="m-1">
            <input v-model="editingGroup.class_year" type="number" placeholder="Номер" class="form-control my-1">
            <input v-model="editingGroup.letter" type="text" placeholder="Буква" class="form-control my-1">
            <input v-model="editingGroup.id_dnevnik" type="text" placeholder="ID Дневник.ру" class="form-control my-1">
            <div class="d-flex justify-content-end">
              <button class="btn-icon img-apply mx-1" :disabled="!(editingGroup.class_year && editingGroup.letter)" @click="groupAdd"></button>
              <button class="btn-icon img-cancel" @click="groupCancel"></button>
            </div>
          </div>
        </div>
        <div v-else>
          Список групп пуст
        </div>
      </div>
      <div class="col-sm">
        <div v-if="currentGroup">
          <div class="mb-2">Список студентов <b>{{ currentGroup.class_year }}{{ currentGroup.letter }}</b> класса</div>
          <div class="mb-2">{{ currentGroup.id_dnevnik }}</div>
          <div class="border p-2" v-if="currentGroup.students.length">
            <div v-for="student in currentGroup.students" :key="student.id" class="student-item">
              <div>{{ student.user.last_name }} {{ student.user.first_name }}</div>
              <button class="ms-auto btn-icon img-remove" @click="deleteStudentFromGroup(student)"></button>
            </div>
          </div>
          <div class="border p-2" v-else>В группе нет студентов</div>
          <div class="mt-2">Добавление студентов:</div>
          <div class="d-flex my-2">
            <input class="form-control" type="search" name="search" id="search" placeholder="Введите студента..."
              v-model="searchValue" @keyup.enter="searchStudents" @search="clearStudents">
            <button class="btn btn-primary ms-2" @click="searchStudents" :disabled="!searchValue">Найти</button>
          </div>
          <div v-if="users.length">
            <div class="border student-list">
              <div class="user-item" v-for="user in filterStudentsSearch(users)" :key="user.id">
                <div>{{ user.last_name }} {{ user.first_name }}</div>
                <button class="ms-auto btn-icon img-append" @click="appendStudentToGroup(user)"></button>
              </div>
            </div>
            <nav aria-label="pagination" class="mt-3 d-flex justify-content-center">
              <ul class="pagination">
                <!-- Ссылка на предыдущую страницу -->
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="prev" @click="changePage(-1)">
                    <span aria-hidden="true">&laquo;</span>
                  </a>
                </li>
                <!-- Ссылка на следующую страницу -->
                <li class="page-item">
                  <a class="page-link" href="#" aria-label="next" @click="changePage(+1)">
                    <span aria-hidden="true">&raquo;</span>
                  </a>
                </li>
              </ul>
            </nav>
          </div>
          <small v-else>
            Для поиска студентов в базе введите фамилию или имя
          </small>
        </div>
        <div v-else class="d-flex justify-content-center align-items-center h-100">Выберите класс</div>
      </div>
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
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { Collapse } from 'bootstrap';
import GroupItem from "@/components/group/GroupItem";
import { getGroups, retrieveGroup, createGroup, updateGroup, deleteGroup } from "@/hooks/user/useGroup";
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getUsers } from "@/hooks/user/useUser";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'GroupBoard',
  components: {
    GroupItem,
  },
  setup(props) {
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { retrievedGroup, fetchRetrieveGroup } = retrieveGroup();
    const { groupedArrayData } = getGroupedArray();
    const { addedGroup, fetchCreateGroup } = createGroup();
    const { updatedGroup, fetchUpdateGroup } = updateGroup();
    const { fetchDeleteGroup } = deleteGroup();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { users, isUserLoading, totalPages, totalUsers, fetchGetUsers } = getUsers();

    return {
      groups, isGroupLoading, fetchGetGroups, groupedArrayData,
      retrievedGroup, fetchRetrieveGroup,
      addedGroup, fetchCreateGroup,
      updatedGroup, fetchUpdateGroup,
      fetchDeleteGroup,
      studyYears, currentStudyYear, fetchGetStudyYears,
      users, isUserLoading, totalPages, totalUsers, fetchGetUsers
    }
  },
  data() {
    return {
      currentYear: null,
      currentGroup: null,
      modeAppendStudents: false,
      searchValue: null,
      currentPage: 1,
      limit: 10,
      editingGroupID: null,
      editingGroup: {},
      deletingGroupID: null,
      addingGroupYear: null,
    }
  },
  methods: {
    getAppendStudents() {
      this.modeAppendStudents = true;
    },
    searchStudents() {
      this.fetchGetUsers({ role: "student", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    clearStudents() {
      this.users = [];
    },
    // Выбор текущего пользователя при нажатии на строку списка
    groupSelect(group) {
      if (this.currentGroup != group) {
        this.fetchRetrieveGroup(group).finally(() => {
          this.currentGroup = this.retrievedGroup;
        })
      } else {
        this.currentGroup = null;
      }
    },
    changePage(page) {
      if (this.currentPage > 1 && this.currentPage < this.totalPages) {
        this.currentPage = this.currentPage + page;
      }
      this.fetchGetUsers({ role: "student", search: this.searchValue, page: this.currentPage, limit: this.limit });
    },
    appendStudentToGroup(user) {
      // this.currentGroup.students.push(user.student);
      this.currentGroup.students_ids = this.currentGroup.students.map(item => item.id)
      this.currentGroup.students_ids.push(user.student.id)
      this.fetchUpdateGroup(this.currentGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup }
      })
    },
    deleteStudentFromGroup(student) {
      this.currentGroup.students = this.currentGroup.students.filter(item => item.id != student.id);
      this.currentGroup.students_ids = this.currentGroup.students.map(item => item.id);
      this.fetchUpdateGroup(this.currentGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup }
      })
    },
    filterStudentsSearch(students) {
      return students.filter(item => !this.currentGroup.students.map(item => item.id).includes(item.student.id))
    },
    showAddGroup(year) {
      if (year) {
        this.addingGroupYear = year;
        this.editingGroup.class_year = year;
      } else {
        this.addingGroupYear = 0;
      }
      
    },
    groupAdd() {
      console.log('Запрос на добавление группы: ', this.editingGroup);
      this.fetchCreateGroup(this.editingGroup).finally(() => {
        const currentClassYear = this.editingGroup.class_year
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${currentClassYear}`);
          new Collapse(collapse, {toggle: false}).show()
          this.editingGroup = {};
          this.addingGroupYear = null;
          this.currentGroup = null
        });
      })
    },
    showUpdateGroup(group) {
      this.editingGroupID = group.id;
      this.editingGroup = { ...group };
    },
    groupEdit() {
      console.log('Запрос на редактирование группы: ', this.editingGroup);
      this.fetchUpdateGroup(this.editingGroup).finally(() => {
        this.currentGroup = { ...this.updatedGroup };
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${this.editingGroup.class_year}`);
          new Collapse(collapse, {toggle: false}).show();
          this.editingGroup = {};
          this.editingGroupID = null;
        }); 
      })
    },
    showDeleteGroup(group) {
      this.deletingGroupID = group.id;
    },
    groupDelete() {
      console.log('Запрос на удаление группы:', this.deletingGroupID);
      const currentClassYear = this.currentGroup.class_year
      this.currentGroup = null;
      this.fetchDeleteGroup(this.deletingGroupID).finally(() => {
        this.fetchGetGroups({ study_year: this.currentYear.id }).finally(() => {
          const collapse = document.querySelector(`#collapse-${currentClassYear}`);
          new Collapse(collapse, {toggle: false}).show()
          this.deletingGroupID = null
        }); 
      })
    },
    groupCancel() {
      this.editingGroup = {};
      this.editingGroupID = null;
      this.deletingGroupID = null;
      this.addingGroupYear = null;
    },
  },
  mounted() {
    this.fetchGetStudyYears().finally(() => {
      this.currentYear = this.currentStudyYear;
      this.fetchGetGroups({ study_year: this.currentYear.id });
    });
  },
  
}
</script>

<style scoped>
@import '@/assets/css/spinner.css';

.select-group {
  background-color: rgb(161, 161, 161) !important;
}

.student-list {}
.student-item {
  display: flex;
  align-items: center;
}
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
  transform: scale(1.2);
}
.img-append {
  background: url('@/assets/img/item-plus.png') no-repeat 50% / 90%;
}
.img-remove {
  background: url('@/assets/img/item-minus.png') no-repeat 50% / 90%;
}
.img-apply {
  background: url('@/assets/img/item-apply.png') no-repeat 50% / 90%;
}
.img-cancel {
  background: url('@/assets/img/item-cancel.png') no-repeat 50% / 90%;
}
</style>