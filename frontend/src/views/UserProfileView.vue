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
                  <input type="file" id="file-upload" @change="handleFileChange" accept="image/jpeg, image/png" style="display: none;"/>
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
                    <p class="mb-0">{{ department }}</p>
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
                    <editable-text class="text-muted" v-model="authStore.user.last_name" propName="last_name" @save="handleSave"/>
                  </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Имя</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-text class="text-muted" v-model="authStore.user.first_name" propName="first_name" @save="handleSave"/>
                  </div>
                </div>
                <hr>
                <div class="row">
                  <div class="col-sm-3">
                    <p class="mb-0">Отчество</p>
                  </div>
                  <div class="col-sm-9">
                    <editable-text class="text-muted" v-model="authStore.user.middle_name" propName="middle_name" @save="handleSave"/>
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
                    <editable-area class="text-muted" v-model="authStore.user.position" propName="position" @save="handleSave"/>
                  </div>
                </div>
              </div>
            </div>
            <!-- <div class="row">
              <div class="col-md-6">
                <div class="card mb-4 mb-md-0">
                  <div class="card-body">
                    <p class="mb-4"><span class="text-primary font-italic me-1">Дополнительные данные</span></p>
                    <p class="mb-1" style="font-size: .77rem;">Web Design</p>
                    <div class="progress rounded" style="height: 5px;">
                      <div class="progress-bar" role="progressbar" style="width: 80%" aria-valuenow="80" aria-valuemin="0"
                        aria-valuemax="100"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div> -->
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from "@/stores/auth";
import imageTeacher from '@/assets/img/teacher.svg'
import resources from "@/services/resources";
import EditableText from "@/common/components/EditableText.vue";
import EditableArea from "@/common/components/EditableArea.vue";

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

const authStore = useAuthStore();

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

