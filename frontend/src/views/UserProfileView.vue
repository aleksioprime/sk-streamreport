<template>
  <div>
    <h1>Профиль пользователя</h1>
    <section>
      <div class="container py-2">
        <div class="row">
          <div class="col-lg-4">
            <div class="card mb-4">
              <div class="card-body text-center">
                <img :src='authStore.user.photo ? authStore.user.photo : imageTeacher' alt="avatar"
                  class="rounded-circle img-fluid photo">
                <h5 class="my-3">{{ authStore.user.full_name }}</h5>
                <div class="d-flex justify-content-center mb-2">
                  <label for="file-upload" class="file-upload btn btn-primary">
                    Загрузить файл
                  </label>
                  <input type="file" id="file-upload" @change="handleFileChange" accept="image/jpeg, image/png"
                    style="display: none;" />
                  <!-- <button type="button" class="btn btn-primary" @click="uploadPhoto" v-if="selectedPhoto">Поменять фотографию</button> -->
                </div>
                <p class="text-muted">Для загрузки фотографии выбирайте файлы формата jpg или png не более 5Мб</p>
              </div>
            </div>
            <div class="card mb-4" v-if="authStore.user.groups.length">
              <div class="card-body p-0">
                <ul class="list-group list-group-flush rounded-3">
                  <li class="list-group-item d-flex justify-content-between align-items-center p-3"
                    v-for="group in authStore.user.groups" :key="group.id">
                    <i class="fas fa-globe fa-lg text-warning"></i>
                    <p class="mb-0">{{ userGroup[group.name] }}</p>
                  </li>
                </ul>
              </div>
            </div>
            <div class="card mb-4" v-if="authStore.user.departments.length">
              <div class="card-body p-0">
                <ul class="list-group list-group-flush rounded-3">
                  <li class="list-group-item d-flex justify-content-between align-items-center p-3"
                    v-for="department in authStore.user.departments" :key="department.id">
                    <i class="fas fa-globe fa-lg text-warning"></i>
                    <p class="mb-0">{{ department.name }}</p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-lg-8">
            <div class="card mb-4">
              <div class="card-body">
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Фамилия</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-text class="text-muted" v-model="authStore.user.last_name" propName="last_name"
                      @save="handleSave" />
                  </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Имя</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-text class="text-muted" v-model="authStore.user.first_name" propName="first_name"
                      @save="handleSave" />
                  </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Отчество</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-text class="text-muted" v-model="authStore.user.middle_name" propName="middle_name"
                      @save="handleSave" />
                  </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Email</p>
                  </div>
                  <div class="col-sm-9">
                    <p class="text-muted mb-0">{{ authStore.user.email }}</p>
                  </div>
                </div>
                <hr>
                <div class="row" v-if="authStore.user.position">
                  <div class="col-sm-3">
                    <p class="mb-0">Должность</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-area class="text-muted" v-model="authStore.user.position" propName="position"
                      @save="handleSave" />
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-4">
              <div class="card-body">
                <div class="mb-2 d-flex align-items-center">
                  <span class="text-primary me-1">Нагрузка</span>
                  <div class="ms-auto">
                    <simple-dropdown title="Выберите учебный год" v-model="currentAcademicYear"
                      :propItems="generalStore.academicYears" showName="name" />
                  </div>
                </div>
                <div>
                  <div v-for="load in authStore.user.teaching_loads" :key="load.id" class="d-flex align-items-center">
                    <div>{{ load.subject.name }}:
                      <span v-for="group, index in load.groups" :key="group.id">{{ group.name }}<span
                          v-if="load.groups.length != index + 1">, </span></span>
                      - <span>{{ load.hours }} час</span>
                    </div>
                    <i class="bi bi-dash-square inline-button ms-2" @click="showConfirmationModal(load)"></i>
                    <confirmation-modal v-if="load.id == currentTeachingLoad.id"
                      :nameModal="`confirmationDeleteTeachingLoad${load.id}`" @confirm="removeTeachingLoad"
                      @cancel="cancelTeachingLoad">
                      Вы действитель хотите удалить эту запись?
                    </confirmation-modal>
                  </div>
                  <div class="mt-3">
                    <a href="javascript:void(0)" @click.prevent="createFormShow" v-if="!createMode">Добавить</a>
                  </div>
                </div>
                <div v-if="createMode">
                  <div class="card card-body">
                    <h5>Добавление предмета в нагрузку на {{ currentAcademicYear.name }}</h5>
                    <small>Внимание! Добавляйте нагрузку для каждого класса отдельно, если они не объединены на внеурочных
                      занятиях</small>
                    <div class="row d-flex align-items-center">
                      <div class="col-md-4">Выберите предмет</div>
                      <div class="col">
                        <search-dropdown class="my-2" title="Предмет не выбран" v-model="newTeachingLoad.subject"
                          :propItems="curriculumStore.subjects" showName="name_level" propName="subject" />
                      </div>
                    </div>
                    <div class="row d-flex align-items-center">
                      <div class="col-md-4">Выберите классы</div>
                      <div class="col">
                        <search-dropdown-multiple class="my-2" title="Не выбрано" v-model="newTeachingLoad.groups"
                          :propItems="generalStore.groups" showName="name" propName="groups" />
                      </div>
                    </div>
                    <div class="row d-flex align-items-center">
                      <div class="col-md-4">Укажите часы</div>
                      <div class="col">
                        <input type="number" class="form-control my-2" v-model="newTeachingLoad.hours"
                          placeholder="Введите кол-во часов">
                      </div>
                    </div>
                    <div class="d-flex items-align-center justify-content-end">
                      <button class="btn btn-success" @click="createTeachingLoad">Добавить</button>
                      <button class="btn btn-secondary ms-2" @click="createFormHide">Отмена</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-4">
              <div class="card-body">
                <p class="mb-2"><span class="text-primary font-italic me-1">Наставничество</span></p>
                <div v-if="authStore.user.mentor_classes.length">Вы являетесь наставником в классах:
                  <strong>
                    <span v-for="group, index in authStore.user.mentor_classes" :key="group.id">{{ group.name }}
                      <span v-if="authStore.user.mentor_classes.length != index + 1">, </span>
                    </span>
                  </strong>
                </div>
                <div v-else>Вы не являетесь наставником</div>
                <div v-if="authStore.user.group_roles.length">Вы связаны с классом в следующих ролях:
                  <ul>
                    <li v-for="gr in authStore.user.group_roles" :key="gr.id">
                      <div><b>{{ gr.group.name }}</b>: {{ gr.role }}</div>
                    </li>
                  </ul>
                </div>
                <div v-else>Вы не связаны ни с каким классом</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue';
import { Modal } from 'bootstrap';


import imageTeacher from '@/assets/img/teacher.svg'
import resources from "@/services/resources";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import SearchDropdownMultiple from "@/common/components/SearchDropdownMultiple.vue";
import EditableText from "@/common/components/EditableText.vue";
import EditableArea from "@/common/components/EditableArea.vue";
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';

const selectedPhoto = ref(null);
const handleFileChange = (event) => {
  selectedPhoto.value = event.target.files[0];
  uploadPhoto();
};

const userGroup = {
  'admin': 'Администратор',
  'employee': 'Учитель',
  'student': 'Студент',
}
const createMode = ref(false)

// Данные создаваемой записи по умолчанию
const defaultTeachingLoad = {
  subject: {},
  groups: [],
  hours: 1,
}

const newTeachingLoad = ref({ ...defaultTeachingLoad })
const currentAcademicYear = ref({})

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

import { useCurriculumStore } from "@/stores/curriculum";
const curriculumStore = useCurriculumStore();

import { useGeneralStore } from "@/stores/general";
const generalStore = useGeneralStore();

const uploadPhoto = async () => {
  if (!selectedPhoto.value) {
    alert("Пожалуйста, выберите файл.");
    return;
  }

  const res = await resources.user.updateUserPhoto(authStore.user.id, selectedPhoto.value);
  if (res.__state === "success") {
    selectedPhoto.value = null
    authStore.setPhoto(res.data.user.photo)
    console.log(res)
  }
}

const handleSave = async (editData) => {
  console.log(`Сохраняемое значение для ${editData.propName}:`, editData.value);
  // Здесь может быть логика для сохранения данных, например, отправка запроса на сервер
  const updatedObject = {
    id: authStore.user.id,
    [editData.propName]: editData.value
  }
  const res = await resources.user.partialUpdateUser(updatedObject);
  if (res.__state === "success") {
    console.log(res)
    await authStore.whoami();
  }
};

// ***** Работа с формой по созданию записи *****

// Появление формы для создания записи
const createFormShow = () => {
  curriculumStore.loadSubjects();
  createMode.value = true;
}

// Скрытие формы для создания записи
const createFormHide = () => {
  createMode.value = false;
  newTeachingLoad.value = { ...defaultTeachingLoad }
}

// Подтверждение создания записи и выполнение запроса
const createTeachingLoad = () => {
  const createdObject = {
    subject: newTeachingLoad.value.subject.id,
    groups: newTeachingLoad.value.groups.map(i => i.id),
    hours: newTeachingLoad.value.hours,
    teacher: authStore.user.id,
    year: currentAcademicYear.value.id,
  };
  console.log(createdObject)
  curriculumStore.createTeachingLoad(createdObject).then((result) => {
    getTeachingLoads();
  }
  );
  newTeachingLoad.value = { ...defaultTeachingLoad }
  createMode.value = false;
}

// ***** Работа с модальным окном для удаления записи *****

const currentTeachingLoad = ref({})
let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной записи
const showConfirmationModal = (load) => {
  currentTeachingLoad.value = load
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteTeachingLoad${load.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной записи и закрыть окно
const cancelTeachingLoad = () => {
  confirmationModal.hide();
  currentTeachingLoad.value = {};
}

// Удалить выбранную запись и закрыть окно
const removeTeachingLoad = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  curriculumStore.removeTeachingLoad(currentTeachingLoad.value.id).then(() => {
    getTeachingLoads();
  })
  confirmationModal.hide();
}

// Запрос на получение списка записей для обновления поля
const getTeachingLoads = () => {
  const config = {
    params: {
      teacher: authStore.user.id,
    }
  }
  curriculumStore.loadTeachingLoads(config).then((result) => {
    console.log(result.data)
    authStore.user.teaching_loads = [...result.data]
  })
}

onMounted(() => {
  generalStore.loadAcademicYears().then(() => {
    currentAcademicYear.value = generalStore.relevantYear;
    generalStore.loadGroups({
      params: {
        year_academic: currentAcademicYear.value.id,
      },
    });
  });
});
</script>

<style lang="scss" scoped>
.photo {
  width: 150px;
  height: 150px;
  object-fit: cover;
}

.file-upload {
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
}
</style>

