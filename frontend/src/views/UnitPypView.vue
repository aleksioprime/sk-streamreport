<template>
  <div>
    <h1>Юниты в PYP</h1>
    <div class="py-2">
      <button type="button" class="btn btn-outline-primary" @click="showUnitPypCreateModal">Создать</button>
      <simple-modal nameModal="unitPypCreateModal" titleConfirm="Создать" titleModal="Создание юнита PYP"
        @confirm="confirmUnitPypCreateModal" @cancel="cancelUnitPypCreateModal">
        <div>
          <div class="my-2">
            <label for="title" class="form-label">Название юнита</label>
            <input v-model="newPypUnit.title" type="text" class="form-control" id="title" placeholder="Название юнита">
            <small class="text-danger">{{ validations.title.error }}</small>
          </div>
          <div class="my-2">
            <label for="hours" class="form-label">Кол-во часов</label>
            <input v-model="newPypUnit.hours" type="number" class="form-control" id="hours" placeholder="Кол-во часов">
            <small class="text-danger">{{ validations.hours.error }}</small>
          </div>
          <div class="my-2">
            <label for="description" class="form-label">Описание юнита</label>
            <textarea v-model="newPypUnit.description" class="form-control" id="description"
              placeholder="Введите описание юнита"></textarea>
          </div>
          <div class="my-2">
            <div class="d-flex align-items-center">
              <label for="year" class="form-label mb-0 me-2">Параллель: </label>
              <simple-dropdown title="Выберите параллель" v-model="newPypUnit.year" :propItems="generalStore.studyYears"
                showName="name" />
            </div>
            <small class="text-danger">{{ validations.year.error }}</small>
          </div>
          <div class="my-2">
            <label for="teachers" class="form-label">Учителя</label>
            <div class="card" id="teachers">
              <div class="card-body">
                <search-dropdown-multiple title="Выберите учителей" v-model="newPypUnit.teachers"
                  :propItems="generalStore.users" showName="short_name" />
              </div>
            </div>
            <small class="text-danger">{{ validations.teachers.error }}</small>
          </div>
          <div class="my-2">
            <div class="d-flex align-items-center">
              <label for="year" class="form-label mb-0 me-2">Трансдисциплинарная тема: </label>
              <simple-dropdown title="Выберите тему" v-model="newPypUnit.transdisciplinary_theme"
                :propItems="unitPypStore.transdisciplinaryThemes" showName="name" />
            </div>
            <small class="text-danger">{{ validations.transdisciplinary_theme.error }}</small>
          </div>
        </div>
      </simple-modal>
    </div>
    <div>
      <div v-for="unit in unitPypStore.pypUnits" :key="unit.id">
        <div class="card my-1">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <h5 class="mb-0">
                <router-link :to="{ name: 'unitPypDetail', params: { id: unit.id } }" class="dropdown-item">
                  {{ unit.title }}</router-link>
              </h5>
              <div class="ms-auto">
                <i class="bi bi-three-dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="##" @click="showConfirmationModal(unit)">Удалить юнит</a>
                  </li>
                </ul>
              </div>
            </div>
            <div>{{ unit.year.name }}</div>
            <div class="my-2">
              <i class="bi bi-person me-1"></i>
              <span v-for="teacher, index in unit.teachers" :key="teacher.id">{{ teacher.short_name }}<span v-if="unit.teachers.length != index + 1">, </span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Подключение модального окна -->
    <confirmation-modal @confirm="removeUnitPypPlanner" @cancel="cancelRemoveUnitPypPlanner">
      Вы действитель хотите удалить PYP юнит:
    </confirmation-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { Modal } from "bootstrap";
import SearchDropdownMultiple from "@/common/components/SearchDropdownMultiple.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import { validateFields, clearValidationErrors } from '@/common/validator'
import { extractIds } from '@/common/helpers/object'

import ConfirmationModal from "@/common/components/ConfirmationModal.vue";
let confirmationModal = null;

import SimpleModal from '@/common/components/SimpleModal.vue';
let unitPypCreateModal = null;

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

import { useGeneralStore } from "@/stores/general";
const generalStore = useGeneralStore();

const currentPypUnit = ref({})

const defaultPypUnit = {
  title: null,
  hours: null,
  description: null,
  teachers: [],
  transdisciplinary_theme: {},
  year: {},
}

const newPypUnit = ref({ ...defaultPypUnit })

const setEmptyValidations = () => ({
  title: {
    error: '',
    rules: ['required']
  },
  hours: {
    error: '',
    rules: ['required']
  },
  teachers: {
    error: '',
    rules: ['required']
  },
  transdisciplinary_theme: {
    error: '',
    rules: ['required']
  },
  year: {
    error: '',
    rules: ['required']
  },
})

const validations = ref(setEmptyValidations())

// ************ Модальное окно создания юнита PYP ************

// Создать и показать модальное окно для создания юнита PYP
const showUnitPypCreateModal = () => {
  generalStore.loadStudyYears();
  generalStore.loadUsers(
    {
      params: {
        groups: 2,
      },
    }
  );
  unitPypStore.loadTransdisciplinaryThemes();
  unitPypCreateModal.show();
}

// Отменить создание юнита и закрыть модальное окно
const cancelUnitPypCreateModal = () => {
  unitPypCreateModal.hide();
  newPypUnit.value = { ...defaultPypUnit };
}

// Подтвердить и отправить запрос на создание юнита PYP
const confirmUnitPypCreateModal = () => {
  if (!validateFields(
    {
      title: newPypUnit.value.title,
      hours: newPypUnit.value.hours,
      teachers: newPypUnit.value.teachers,
      transdisciplinary_theme: newPypUnit.value.transdisciplinary_theme,
      year: newPypUnit.value.year,
    },
    validations.value
  )) {
    return
  }
  const createdObject = extractIds(newPypUnit.value);
  console.log('Создание юнита PYP: ', createdObject)
  unitPypStore
    .createPypUnitPlanner(createdObject)
    .then((res) => {
      if (res.__state === "success") {
        unitPypStore.loadPypUnitPlanners();
      } else {
        console.log(res)
      }
    })
  unitPypCreateModal.hide();
  newPypUnit.value = { ...defaultPypUnit };
}

// Открытие модального окна для подтверждения удаления
const showConfirmationModal = (unit) => {
  currentPypUnit.value = unit;
  confirmationModal.show();
};

const removeUnitPypPlanner = () => {
  // console.log('Запрос на удаление юнита PYP: ', currentPypUnit.value);
  unitPypStore
    .removePypUnitPlanner(currentPypUnit.value.id)
    .then((result) => {
      // console.log('Юнит успешно удалён: ', result);
      unitPypStore.loadPypUnitPlanners();
    });
  confirmationModal.hide();
};

const cancelRemoveUnitPypPlanner = () => {
  confirmationModal.hide();
  currentPypUnit.value = {};
};

onMounted(() => {
  unitPypStore.loadPypUnitPlanners();

  confirmationModal = new Modal("#confirmationModal", { backdrop: "static" });
  unitPypCreateModal = new Modal("#unitPypCreateModal", { backdrop: "static" });
});

</script>