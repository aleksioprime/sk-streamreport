<template>
  <div>
    <h5>Участие в мероприятиях</h5>
    <div v-if="report.student.student_events && report.student.student_events.length">
      <table class="table table-sm table-bordered">
        <thead>
          <tr>
            <th scope="col" style="width: 40%;">Название</th>
            <th scope="col" style="min-width: 120px;">Даты</th>
            <th scope="col" style="width: 60%;">Результат</th>
            <th style="min-width: 30px;"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in report.student.student_events" :key="event.id">
            <td>
              <editable-text-cell :propData="event.title" propName="title" @save="handleSave($event, event.id)" />
            </td>
            <td>
              <div class="d-flex flex-column">
                <editable-date-cell :propDate="event.date_start" propName="date_start" @save="handleSave($event, event.id)"/>
                <editable-date-cell :propDate="event.date_end" propName="date_end" @save="handleSave($event, event.id)"/>
              </div>
            </td>
            <td>
              <editable-textarea-cell :propData="event.result" propName="result" @save="handleSave($event, event.id)" />
            </td>
            <td>
              <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(event)"></i>
              <confirmation-modal v-if="event.id == currentEventParticipation.id"
                :nameModal="`confirmationDeleteEvent${event.id}`" @confirm="removeEventParticipation"
                @cancel="cancelEventParticipation">
                Вы действитель хотите удалить эту тему?
              </confirmation-modal>
            </td>
          </tr>
        </tbody>
      </table>
      <a href="##" @click="createFormShow">Добавить</a>
    </div>

    <div class="card" v-else>
      <div class="card-body">
        <div class="d-flex flex-column align-items-center">
          <div>У студента нет участий в мероприятиях</div>
          <a href="##" @click="createFormShow">Добавить</a>
        </div>
      </div>
    </div>
    <div v-if="createMode">
      <div class="card my-2">
        <div class="card-body">
          <div class="row g-3 align-items-center">
            <div class="col-auto">
              <label :for="`date-${report.id}`" class="col-form-label">Выберите даты:</label>
            </div>
            <div class="col-auto">
              <div :id="`date-${report.id}`" class="btn-group">
                <button type="button" class="btn btn-outline-secondary">
                  <span v-if="newEventParticipate.dateRange.start && newEventParticipate.dateRange.end">
                    {{ newEventParticipate.dateRange.start.toLocaleDateString() }}
                    - {{ newEventParticipate.dateRange.end.toLocaleDateString() }}
                  </span>
                  <span v-else>Не выбраны даты</span>
                </button>
                <button class="btn btn-secondary dropdown-toggle dropdown-toggle-split" type="button"
                  data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
                  <span class="visually-hidden">Toggle Dropdown</span>
                </button>
                <div class="dropdown-menu p-0 border-0 text-body-secondary">
                  <div>
                    <VDatePicker v-model.range="newEventParticipate.dateRange" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <input v-model="newEventParticipate.title" type="text" class="form-control my-2"
            placeholder="Введите название мероприятия">
          <textarea v-model="newEventParticipate.result" class="form-control bottom-border-only my-2" rows="3"
            placeholder="Опишите результаты участия"></textarea>
          <div class="d-flex items-align-center justify-content-end">
            <button class="btn btn-success" @click="createEventParticipation">Добавить</button>
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

import EditableTextareaCell from "@/common/components/EditableTextareaCell.vue";
import EditableTextCell from "@/common/components/EditableTextCell.vue";
import EditableDateCell from "@/common/components/EditableDateCell.vue";
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';

import { useAuthStore } from "@/stores/auth";
import { usePortfolioStore } from "@/stores/portfolio";

import { formatToYYYYMMDD, formatDateToReadable } from "@/common/helpers/date.js";

const props = defineProps({
  report: {
    type: Object,
    default: {}
  },
});

const authStore = useAuthStore();
const portfolioStore = usePortfolioStore();

const createMode = ref(false)

const defaultEventParticipate = {
  title: null,
  result: null,
  dateRange: {
    start: null,
    end: null,
  },
}

const newEventParticipate = ref({ ...defaultEventParticipate })
const currentEventParticipation = ref({})

const createFormShow = () => {
  createMode.value = true;
}

const createFormHide = () => {
  createMode.value = false;
  newEventParticipate.value = { ...defaultEventParticipate }
}

// Создание мероприятия
const createEventParticipation = () => {
  const {
    title,
    result,
    dateRange: { start, end }
  } = newEventParticipate.value;

  const createdObject = {
    group: props.report.group.id,
    student: props.report.student.id,
    author: authStore.user.id,
    title,
    result,
    date_start: formatToYYYYMMDD(start),
    date_end: formatToYYYYMMDD(end) || formatToYYYYMMDD(start),
  };

  console.log('Создание объекта: ', createdObject);

  portfolioStore.createEventParticipation(createdObject).then((res) => {
    if (res.__state === "success") {
      getEventParticipations();
    } else {
      console.log(res)
    }
    createFormHide();
  })
}

// ************ Модальное окно для удаления выбранного участия в мероприятии ************

let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной темы из репорта
const showConfirmationModal = (event) => {
  currentEventParticipation.value = event
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteEvent${event.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной темы из репорта и закрыть окно
const cancelEventParticipation = () => {
  confirmationModal.hide();
  currentEventParticipation.value = {};
}

// Удалить участие в мероприятии и закрыть окно
const removeEventParticipation = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  portfolioStore.removeEventParticipation(currentEventParticipation.value.id).then(() => {
    getEventParticipations();
  })
  confirmationModal.hide();
}

// Получить участия в мероприятиях студента класса для дальнейшей замены данных списка репортов
const getEventParticipations = () => {
  const config = {
    params: {
      student: props.report.student.id,
      group: props.report.group.id,
    },
  };
  portfolioStore.loadEventParticipations(config).then((result) => {
    console.log(result)
    props.report.student.student_events = [...result.data];
  });
};

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для участия в мероприятии с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  portfolioStore.updateEventParticipation(updatingData).then((result) => {
    console.log('Результаты участия в мероприятии успешно обновлены: ', result);
    // Перезапись отредактированного объекта в report
    props.report.student.student_events = props.report.student.student_events.map(item => item.id === result.data.id ? { ...result.data } : item);
  })
};

onMounted(() => {

})
</script>

<style scoped></style>