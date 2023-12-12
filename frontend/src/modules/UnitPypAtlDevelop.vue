<template>
  <div>
    <div v-if="unit.atl_develops.length">
      <!-- Таблица вывода существующих записей -->
      <table class="table table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col" style="width: 40%;">Навык</th>
            <th scope="col" style="width: 60%;">Действия</th>
            <th scope="col" style="min-width: 30px;"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="atl in unit.atl_develops" :key="atl.id">
            <td><b>{{ atl.atl.cluster.name }}:</b> {{ atl.atl.name }}</td>
            <td>
              <editable-textarea-cell :propData="atl.action" propName="action" @save="handleSave($event, atl.id)" />
            </td>
            <td>
              <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(atl)"></i>
              <confirmation-modal v-if="atl.id == currentAtlDevelop.id"
                :nameModal="`confirmationDeleteAtlDevelop${atl.id}`" @confirm="removeAtlDevelop"
                @cancel="cancelAtlDevelop">
                Вы действитель хотите удалить эту запись?
              </confirmation-modal>
            </td>
          </tr>
        </tbody>
      </table>
      <a href="##" @click="createFormShow">Добавить</a>
    </div>
    <div class="card" v-else>
      <!-- Сообщение о том, что данных нет -->
      <div class="card-body">
        <div class="d-flex flex-column align-items-center">
          <div>Нет информации</div>
          <a href="##" @click="createFormShow">Добавить</a>
        </div>
      </div>
    </div> 
    <!-- Форма добавления новой записи в таблицу -->
    <div v-if="createMode">
      <div class="card my-2">
        <div class="card-body">
          <simple-dropdown class="my-2" title="Выберите кластер ATL" v-model="currentCluster"
            :propItems="unitPypStore.pypAtlClusters" showName="name" @select="selectCluster" />
          <search-dropdown class="my-2" title="Выберите навык ATL" v-model="newAtlDevelop.atl"
            :propItems="unitPypStore.pypAtlSkills" showName="name" propName="atl" />
          <textarea v-model="newAtlDevelop.action" class="form-control bottom-border-only my-2" rows="3"
            placeholder="Опишите действия"></textarea>
          <div class="d-flex items-align-center justify-content-end">
            <button class="btn btn-success" @click="createAtlDevelop">Добавить</button>
            <button class="btn btn-secondary ms-2" @click="createFormHide">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import SearchDropdown from "@/common/components/SearchDropdown.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import EditableTextareaCell from "@/common/components/EditableTextareaCell.vue";

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

const props = defineProps({
  unit: {
    type: Object,
    default: {}
  },
});

const createMode = ref(false)

// Выбор кластера из выпадающего списка
const currentCluster = ref({})
const selectCluster = () => {
  newAtlDevelop.atl = {}
  unitPypStore.loadPypAtlSkills({
    params: {
      cluster: currentCluster.value.id,
    }
  });
}

// Данные создаваемой записи по умолчанию
const defaultAtlDevelop = {
  atl: null,
  action: null,
}
const newAtlDevelop = ref({ ...defaultAtlDevelop })


// ***** Работа с формой по созданию записи *****

// Появление формы для создания записи
const createFormShow = () => {
  createMode.value = true;
}

// Скрытие формы для создания записи
const createFormHide = () => {
  createMode.value = false;
  newAtlDevelop.value = { ...defaultAtlDevelop }
  currentCluster.value = {}
  unitPypStore.pypAtlSkills = []
}

// Подтверждение создания записи и выполнение запроса
const createAtlDevelop = () => {
  const createdObject = {
    atl: newAtlDevelop.value.atl.id,
    action: newAtlDevelop.value.action,
    unit: props.unit.id
  };
  unitPypStore.createPypAtlDevelop(createdObject).then((result) => {
    getAtlDevelops();
  }
  );
  console.log('Создание объекта: ', createdObject);
  currentCluster.value = {}
  unitPypStore.pypAtlSkills = []
  newAtlDevelop.value = { ...defaultAtlDevelop }
  createMode.value = false;
}

// ***** Работа с модальным окном для удаления записи *****

const currentAtlDevelop = ref({})
let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной записи
const showConfirmationModal = (atl) => {
  currentAtlDevelop.value = atl
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteAtlDevelop${atl.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной записи и закрыть окно
const cancelAtlDevelop = () => {
  confirmationModal.hide();
  currentAtlDevelop.value = {};
}

// Удалить выбранную запись и закрыть окно
const removeAtlDevelop = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  unitPypStore.removePypAtlDevelop(currentAtlDevelop.value.id).then(() => {
    getAtlDevelops();
  })
  confirmationModal.hide();
}

// Запрос на получение списка записей для обновления поля
const getAtlDevelops = () => {
  const config = {
    params: {
      unit: props.unit.id
    }
  }
  unitPypStore.loadPypAtlDevelops(config).then((result) => {
    unitPypStore.pypUnit.atl_develops = [...result.data]
  })
}

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  unitPypStore.updatePypAtlDevelop(updatingData).then((result) => {
    unitPypStore.pypUnit.atl_develops = unitPypStore.pypUnit.atl_develops.map(item => item.id === result.data.id ? { ...result.data } : item);
  })
};

</script>