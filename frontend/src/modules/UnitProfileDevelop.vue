<template>
  <div>
    <div v-if="unit.ibprofiles.length">
      <!-- Таблица вывода существующих записей -->
      <table class="table table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col" style="min-width: 140px;">Профиль</th>
            <th scope="col" style="width: 100%;">Описание</th>
            <th scope="col" style="min-width: 30px;"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="profile in unit.ibprofiles" :key="profile.id">
            <td>{{ profile.profile.name }}</td>
            <td>
              <editable-textarea-cell :propData="profile.description" propName="description" @save="handleSave($event, profile.id)" />
            </td>
            <td>
              <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(profile)"></i>
              <confirmation-modal v-if="profile.id == currentIbProfileDevelop.id"
                :nameModal="`confirmationDeleteIbProfileDevelop${profile.id}`" @confirm="removeIbProfileDevelop"
                @cancel="cancelIbProfileDevelop">
                Вы действитель хотите удалить эту запись?
              </confirmation-modal>
            </td>
          </tr>
        </tbody>
      </table>
      <a href="javascript:void(0)" @click.prevent="createFormShow">Добавить</a>
    </div>
    <div class="card" v-else>
      <!-- Сообщение о том, что данных нет -->
      <div class="card-body">
        <div class="d-flex flex-column align-items-center">
          <div>Нет информации</div>
          <a href="javascript:void(0)" @click.prevent="createFormShow">Добавить</a>
        </div>
      </div>
    </div> 
    <!-- Форма добавления новой записи в таблицу -->
    <div v-if="createMode">
      <div class="card my-2">
        <div class="card-body">
          <search-dropdown class="my-2" title="Выберите профиль" v-model="newIbProfileDevelop.profile"
            :propItems="iboStore.learnerProfiles" showName="name" propName="profile" />
          <textarea v-model="newIbProfileDevelop.description" class="form-control bottom-border-only my-2" rows="3"
            placeholder="Опишите развитие выбранного навыка"></textarea>
          <div class="d-flex items-align-center justify-content-end">
            <button class="btn btn-success" @click="createIbProfileDevelop">Добавить</button>
            <button class="btn btn-secondary ms-2" @click="createFormHide">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { Modal } from 'bootstrap';

import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import EditableTextareaCell from "@/common/components/EditableTextareaCell.vue";

import { useIboStore } from "@/stores/ibo";
const iboStore = useIboStore();

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

const props = defineProps({
  unit: {
    type: Object,
    default: {}
  },
});

const createMode = ref(false)

// Данные создаваемой записи по умолчанию
const defaultIbProfileDevelop = {
  profile: {},
  description: null,
}
const newIbProfileDevelop = ref({ ...defaultIbProfileDevelop })

// ***** Работа с формой по созданию записи *****

// Появление формы для создания записи
const createFormShow = () => {
  createMode.value = true;
}

// Скрытие формы для создания записи
const createFormHide = () => {
  createMode.value = false;
  newIbProfileDevelop.value = { ...defaultIbProfileDevelop }
}

// Подтверждение создания записи и выполнение запроса
const createIbProfileDevelop = () => {
  const createdObject = {
    profile: newIbProfileDevelop.value.profile.id,
    description: newIbProfileDevelop.value.description,
    unit: props.unit.id
  };
  iboStore.createIbProfileDevelop(createdObject).then((result) => {
    getIbProfileDevelops();
  }
  );
  newIbProfileDevelop.value = { ...defaultIbProfileDevelop }
  createMode.value = false;
}

// ***** Работа с модальным окном для удаления записи *****

const currentIbProfileDevelop = ref({})
let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной записи
const showConfirmationModal = (profile) => {
  currentIbProfileDevelop.value = profile
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteIbProfileDevelop${profile.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной записи и закрыть окно
const cancelIbProfileDevelop = () => {
  confirmationModal.hide();
  currentIbProfileDevelop.value = {};
}

// Удалить выбранную запись и закрыть окно
const removeIbProfileDevelop = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  iboStore.removeIbProfileDevelop(currentIbProfileDevelop.value.id).then(() => {
    getIbProfileDevelops();
  })
  confirmationModal.hide();
}

// Запрос на получение списка записей для обновления поля
const getIbProfileDevelops = () => {
  const config = {
    params: {
      unit: props.unit.id
    }
  }
  iboStore.loadIbProfileDevelops(config).then((result) => {
    unitPypStore.pypUnit.ibprofiles = [...result.data]
  })
}

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  iboStore.updateIbProfileDevelop(updatingData).then((result) => {
    unitPypStore.pypUnit.ibprofiles = unitPypStore.pypUnit.ibprofiles.map(item => item.id === result.data.id ? { ...result.data } : item);
  })
};
</script>