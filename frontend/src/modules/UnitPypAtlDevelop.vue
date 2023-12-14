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
          <template v-for="atl in unit.atl_develops" :key="atl.id">
            <tr>
              <td>
                <div><b>{{ atl.category.name.toUpperCase() }}</b><i class="bi bi-pencil-square inline-button ms-2"
                    @click="toggleEditMode"></i></div>
                <div v-if="atl.cluster">{{ atl.cluster.name }}</div>
                <div v-if="atl.skill">{{ atl.skill.name }}</div>
              </td>
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
            <tr v-if="editMode">
              <td colspan="3">
                <div class="d-flex">
                  <simple-dropdown class="my-2" title="Выберите кластер" v-model="atl.cluster"
                    :propItems="unitPypStore.pypAtlClusters.filter(i => i.category.id == atl.category.id)"
                    propName="cluster" showName="name" @select="handleSave($event, atl.id)" />
                  <i class="bi bi-x-square ms-auto inline-button" @click="editMode = false"></i>
                </div>
                <simple-dropdown class="my-2" title="Выберите навык" v-model="atl.skill"
                  :propItems="unitPypStore.pypAtlSkills.filter(i => i.cluster.id == atl.cluster.id)" propName="skill"
                  showName="name" @select="handleSave($event, atl.id)" />
              </td>
            </tr>
          </template>
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
    <div v-if="createMode" id="createATL">
      <div class="card my-2">
        <div class="card-body">
          <div class="d-flex">
            <simple-dropdown class="my-2 me-2" title="Выберите категорию ATL" v-model="newAtlDevelop.category"
              :propItems="iboStore.atlCategories" showName="name" propName="category" @select="selectCategory" />
            <simple-dropdown class="my-2" title="Выберите кластер ATL" v-model="newAtlDevelop.cluster"
              :propItems="unitPypStore.pypAtlClusters" showName="name" propName="cluster" @select="selectCluster"
              :disabled="!newAtlDevelop.category.id" />
          </div>
          <search-dropdown class="my-2" title="Выберите навык ATL" v-model="newAtlDevelop.skill"
            :propItems="unitPypStore.pypAtlSkills" showName="name" propName="skill"
            :disabled="!newAtlDevelop.cluster.id" />
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

import { useIboStore } from "@/stores/ibo";
const iboStore = useIboStore();

const props = defineProps({
  unit: {
    type: Object,
    default: {}
  },
});

const editMode = ref(false)

const createMode = ref(false)

const toggleEditMode = () => {
  unitPypStore.loadPypAtlClusters();
  unitPypStore.loadPypAtlSkills();
  if (!editMode.value) {
    editMode.value = true
  } else {
    editMode.value = false
  }
}

const currentCategory = ref({})
const selectCategory = () => {
  newAtlDevelop.cluster = {}
  unitPypStore.loadPypAtlClusters({
    params: {
      category: newAtlDevelop.value.category.id,
    }
  });
}

// Выбор кластера из выпадающего списка
const currentCluster = ref({})
const selectCluster = () => {
  newAtlDevelop.skill = {}
  unitPypStore.loadPypAtlSkills({
    params: {
      cluster: newAtlDevelop.value.cluster.id,
    }
  });
}

// Данные создаваемой записи по умолчанию
const defaultAtlDevelop = {
  category: {},
  cluster: {},
  skill: {},
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
    category: newAtlDevelop.value.category.id,
    cluster: newAtlDevelop.value.cluster.id,
    skill: newAtlDevelop.value.skill.id,
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