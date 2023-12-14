<template>
    <div>
      <div v-if="unit.related_concepts.length">
        <!-- Таблица вывода существующих записей -->
        <table class="table table-sm table-bordered">
          <thead>
            <tr>
              <th scope="col" style="width: 100%;">Сопутствующий концепт</th>
              <th scope="col" style="min-width: 30px;"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rc in unit.related_concepts" :key="rc.id">
              <td>
                <editable-text-cell :propData="rc.name" propName="name" @save="handleSave($event, rc.id)" />
              </td>
              <td>
                <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(rc)"></i>
                <confirmation-modal v-if="rc.id == currentPypRelatedConcept.id"
                  :nameModal="`confirmationDeletePypRelatedConcept${rc.id}`" @confirm="removePypRelatedConcept"
                  @cancel="cancelPypRelatedConcept">
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
            <input type="text" class="form-control my-2" v-model="newPypRelatedConcept.name" placeholder="Введите сопутствующий концепт">
            <div class="d-flex items-align-center justify-content-end">
              <button class="btn btn-success" @click="createPypRelatedConcept">Добавить</button>
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
  import EditableTextCell from "@/common/components/EditableTextCell.vue";
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
  const defaultPypRelatedConcept = {
    name: null,
    key_concept: {},
  }
  const newPypRelatedConcept = ref({ ...defaultPypRelatedConcept })
  
  // ***** Работа с формой по созданию записи *****
  
  // Появление формы для создания записи
  const createFormShow = () => {
    createMode.value = true;
  }
  
  // Скрытие формы для создания записи
  const createFormHide = () => {
    createMode.value = false;
    newPypRelatedConcept.value = { ...defaultPypRelatedConcept }
  }
  
  // Подтверждение создания записи и выполнение запроса
  const createPypRelatedConcept = () => {
    const createdObject = {
      name: newPypRelatedConcept.value.name,
      unit: props.unit.id
    };
    unitPypStore.createPypRelatedConcept(createdObject).then((result) => {
      getPypRelatedConcepts();
    }
    );
    console.log('Создание объекта: ', createdObject);
    createMode.value = false;
    newPypRelatedConcept.value = { ...defaultPypRelatedConcept };
  }
  
  // ***** Работа с модальным окном для удаления записи *****
  
  const currentPypRelatedConcept = ref({})
  let confirmationModal = null
  
  // Открыть модальное окно для подтверждения удаления выбранной записи
  const showConfirmationModal = (loi) => {
    currentPypRelatedConcept.value = loi
    nextTick(() => {
      confirmationModal = new Modal(`#confirmationDeletePypRelatedConcept${loi.id}`, { backdrop: 'static' });
      confirmationModal.show();
    });
  }
  
  // Отменить удаление выбранной записи и закрыть окно
  const cancelPypRelatedConcept = () => {
    confirmationModal.hide();
    currentPypRelatedConcept.value = {};
  }
  
  // Удалить выбранную запись и закрыть окно
  const removePypRelatedConcept = () => {
    // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
    unitPypStore.removePypRelatedConcept(currentPypRelatedConcept.value.id).then(() => {
      getPypRelatedConcepts();
    })
    confirmationModal.hide();
  }
  
  // Запрос на получение списка записей для обновления поля
  const getPypRelatedConcepts = () => {
    const config = {
      params: {
        unit: props.unit.id
      }
    }
    unitPypStore.loadPypRelatedConcepts(config).then((result) => {
      unitPypStore.pypUnit.related_concepts = [...result.data]
    })
  }
  
  // Функция редактирования конкретного поля
  const handleSave = async (editData, id) => {
    const updatingData = {
      id: id,
      [editData.propName]: editData.value,
    }
    unitPypStore.updatePypRelatedConcept(updatingData).then((result) => {
      unitPypStore.pypUnit.related_concepts = unitPypStore.pypUnit.related_concepts.map(item => item.id === result.data.id ? { ...result.data } : item);
    })
  };
  
  
  </script>