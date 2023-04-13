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
                <group-item v-for="group in groupsByYear" :key="group.id" :group="group" @select="groupSelect"
                  :class="[currentGroup == group ? 'select-group' : '']" class="border my-1" />
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          Список групп пуст
        </div>
      </div>
      <div class="col-sm">
        <div v-if="currentGroup">
          <div class="mb-2">Список студентов {{ currentGroup.class_year }}{{ currentGroup.letter }} класса</div>
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
        <div v-else>Выберите класс</div>
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
import GroupItem from "@/components/group/GroupItem";
import StudentItem from "@/components/group/StudentItem";
import { getGroups, retrieveGroup, createGroup, updateGroup, deleteGroup } from "@/hooks/user/useGroup";
import { getStudyYears } from "@/hooks/assess/useStudyYear";
import { getUsers } from "@/hooks/user/useUser";
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'GroupBoard',
  components: {
    GroupItem, StudentItem
  },
  setup(props) {
    const { groups, isGroupLoading, fetchGetGroups } = getGroups();
    const { retrievedGroup, fetchRetrieveGroup } = retrieveGroup();
    const { groupedArrayData } = getGroupedArray();
    const { fetchCreateGroup } = createGroup();
    const { updatedGroup, fetchUpdateGroup } = updateGroup();
    const { fetchDeleteGroup } = deleteGroup();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();
    const { users, isUserLoading, totalPages, totalUsers, fetchGetUsers } = getUsers();

    return {
      groups, isGroupLoading, fetchGetGroups, groupedArrayData,
      retrievedGroup, fetchRetrieveGroup,
      fetchCreateGroup,
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
    }
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
  transform: scale(1.1);
}

.img-append {
  background: url('@/assets/img/item-plus.png') no-repeat 50% / 90%;
}

.img-remove {
  background: url('@/assets/img/item-minus.png') no-repeat 50% / 90%;
}</style>