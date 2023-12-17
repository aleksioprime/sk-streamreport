<template>
  <div>
    <div v-if="unit.inquiry_lines.length">
      <!-- Таблица вывода существующих записей -->
      <table class="table table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col" style="min-width: 180px;">Ключевой концепт</th>
            <th scope="col" style="width: 100%;">Линия исследования</th>
            <th scope="col" style="min-width: 30px;"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="il in unit.inquiry_lines" :key="il.id">
            <td>
              <simple-dropdown class="my-2" title="Выберите ключевой концепт" v-model="il.key_concept"
                :propItems="filteredPypKeyConcepts" propName="key_concept" showName="name_rus" @select="handleSave($event, il.id)" />
            </td>
            <td>
              <editable-text-cell :propData="il.name" propName="name" @save="handleSave($event, il.id)" />
            </td>
            <td>
              <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(il)"></i>
              <confirmation-modal v-if="il.id == currentLinesOfInquiry.id"
                :nameModal="`confirmationDeleteLinesOfInquiry${il.id}`" @confirm="removeLinesOfInquiry"
                @cancel="cancelLinesOfInquiry">
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
          <input type="text" class="form-control my-2" v-model="newLinesOfInquiry.name" placeholder="Напишите линию исследования">
          <simple-dropdown class="my-2" title="Выберите ключевой концепт" v-model="newLinesOfInquiry.key_concept"
            :propItems="filteredPypKeyConcepts" showName="name_rus"/>
          <div class="d-flex items-align-center justify-content-end">
            <button class="btn btn-success" @click="createLinesOfInquiry">Добавить</button>
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
import EditableTextCell from "@/common/components/EditableTextCell.vue";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
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
const defaultLinesOfInquiry = {
  name: null,
  key_concept: {},
}
const newLinesOfInquiry = ref({ ...defaultLinesOfInquiry })

const filteredPypKeyConcepts = computed(() => {
  return unitPypStore.pypKeyConcepts.filter((item) => {
    return props.unit.key_concepts.map(i => i.id).includes(item.id)
  })
})


// ***** Работа с формой по созданию записи *****

// Появление формы для создания записи
const createFormShow = () => {
  createMode.value = true;
}

// Скрытие формы для создания записи
const createFormHide = () => {
  createMode.value = false;
  newLinesOfInquiry.value = { ...defaultLinesOfInquiry }
}

// Подтверждение создания записи и выполнение запроса
const createLinesOfInquiry = () => {
  const createdObject = {
    name: newLinesOfInquiry.value.name,
    key_concept: newLinesOfInquiry.value.key_concept ? newLinesOfInquiry.value.key_concept.id : null,
    unit: props.unit.id
  };
  unitPypStore.createPypLinesOfInquiry(createdObject).then((result) => {
    authStore.showMessageSuccess('Линия исследования добавлена');
    getLinesOfInquiries();
  }
  );
  console.log('Создание объекта: ', createdObject);
  createMode.value = false;
  newLinesOfInquiry.value = { ...defaultLinesOfInquiry };
}

// ***** Работа с модальным окном для удаления записи *****

const currentLinesOfInquiry = ref({})
let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной записи
const showConfirmationModal = (loi) => {
  currentLinesOfInquiry.value = loi
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteLinesOfInquiry${loi.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной записи и закрыть окно
const cancelLinesOfInquiry = () => {
  confirmationModal.hide();
  currentLinesOfInquiry.value = {};
}

// Удалить выбранную запись и закрыть окно
const removeLinesOfInquiry = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  unitPypStore.removePypLinesOfInquiry(currentLinesOfInquiry.value.id).then(() => {
    authStore.showMessageSuccess('Линия исследования удалена');
    getLinesOfInquiries();
  })
  confirmationModal.hide();
}

// Запрос на получение списка записей для обновления поля
const getLinesOfInquiries = () => {
  const config = {
    params: {
      unit: props.unit.id
    }
  }
  unitPypStore.loadPypLinesOfInquiries(config).then((result) => {
    unitPypStore.pypUnit.inquiry_lines = [...result.data]
  })
}

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  unitPypStore.updatePypLinesOfInquiry(updatingData).then((result) => {
    authStore.showMessageSuccess('Сохранено');
    unitPypStore.pypUnit.inquiry_lines = unitPypStore.pypUnit.inquiry_lines.map(item => item.id === result.data.id ? { ...result.data } : item);
  })
};


</script>