<template>
  <div class="my-3">
    <div class="d-flex align-items-center mb-2">
      <h5>Достижения в исследовательской деятельности</h5>
      <div class="ms-auto" v-if="allowedMode">
        <i class="bi bi-three-dots dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="javascript:void(0)" @click.prevent="showUnitImportModal(report)">Добавить юниты</a></li>
        </ul>
      </div>
    </div>
    <div v-if="report.pyp_units.length">
      <div v-for="unit in report.pyp_units" :key="unit.id" class="d-flex align-items-center my-2">
        <div class="card card-body">
          <div class="d-flex align-items-center" >
            <div><b>{{ unit.unit.title }}</b> ({{ unit.unit.year.number }} классы)</div>
            <i class="bi bi-dash-square dot-menu ms-auto" v-if="allowedMode" @click="showConfirmationModal(unit)"></i>
          </div>
          <div class="my-2">
              <i class="bi bi-person me-1"></i>
              <span v-for="teacher, index in unit.unit.teachers" :key="teacher.id">{{ teacher.short_name }}<span v-if="unit.unit.teachers.length != index + 1">, </span></span>
            </div>
          <hr>
          <div class="my-2">
            <editable-area v-model="unit.comment" propName="comment" @save="handleSave($event, unit.id)" :allowedMode="allowedMode"/>
          </div>
          <div>
            <confirmation-modal v-if="unit.id == currentPrimaryUnit.id" :nameModal="`confirmationDeleteUnit${unit.id}`"
              @confirm="removePrimaryUnit" @cancel="cancelRemovePrimaryUnit">
              Вы действитель хотите удалить этот юнит?
            </confirmation-modal>
          </div>
        </div>
      </div>
    </div>
    <div class="card" v-else>
      <div class="card-body">
        <div class="d-flex justify-content-center">
          Достижений в исследовательской деятельности пока нет
        </div>
      </div>
    </div>
    <simple-modal v-if="report.id == currentReport.id" :nameModal="`unitImportModal${report.id}`"
      titleConfirm="Добавить темы" titleModal="Добавление юнитов в репорт студента" @confirm="confirmUnitImportModal"
      @cancel="cancelUnitImportModal">
      <div>
        <div v-if="unitPypStore.pypUnits.length">
          <div class="form-check" v-for="unit in unitPypStore.pypUnits" :key="unit.id">
            <input class="form-check-input" type="checkbox" :value="unit.id" :id="`check-${unit.id}`"
              v-model="choiceUnits" :disabled="checkDisableUnit(unit.id)">
            <label class="form-check-label" :for="`check-${unit.id}`">
              {{ unit.year.name }}: {{ unit.order }}. {{ unit.title }} 
            </label>
          </div>
        </div>
        <div v-else class="my-2">Учебных тем для импорта не найдено</div>
      </div>
    </simple-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import EditableArea from "@/common/components/EditableArea.vue";
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import SimpleModal from '@/common/components/SimpleModal.vue';

const props = defineProps({
  report: {
    type: Object,
    default: {}
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

import { useReportStore } from "@/stores/report";
const reportStore = useReportStore();

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

let confirmationModal = null
let unitImportModal = null

const currentPrimaryUnit = ref({})
const currentReport = ref({})
const choiceUnits = ref([])

// Условие отключения чекбокса для темы, которая уже была добавлена в репорт
const checkDisableUnit = (id) => {
  return props.report.pyp_units.some(item => item.unit.id == id)
}

// ************ Модальное окно для добавления юнитов в репорт ************

// Создать и показать модальное окно для добавления в репорт выделенных юнитов
// Сделать запрос на вывод в модальное окно юнитов в PYP
const showUnitImportModal = (report) => {
  currentReport.value = report
  nextTick(() => {
    unitImportModal = new Modal(`#unitImportModal${report.id}`, { backdrop: 'static' });
    unitImportModal.show();
  });
  unitPypStore.loadPypUnitPlanners({
    params: {
    }
  })
}

// Отменить добавление в репорт юнитов и закрыть модальное окно
const cancelUnitImportModal = () => {
  unitImportModal.hide();
  choiceUnits.value = [];
  currentReport.value = {};
}

// Подтвердить и отправить запрос на добавление выбранных юнитов в репорт студента
// Запросить обновлённый список юнитов из репорта и заменить переменную в reportStore
const confirmUnitImportModal = () => {
  // console.log('Добавление тем в репорт студента: ', choiceTopics.value)
  unitImportModal.hide();
  const creatingData = choiceUnits.value.map(item => ({
    unit: item,
    report: props.report.id
  }));
  reportStore.createReportMentorPrimaryUnit(creatingData).then((result) => {
    authStore.showMessageSuccess('Данные юнита добавлены');
    getReportPrimaryUnits();
  })
  choiceUnits.value = [];
  currentReport.value = {};
}

// ************ Модальное окно для удаления выбранного юнита из репорта ************

// Открыть модальное окно для подтверждения удаления выбранного юнита
const showConfirmationModal = (unit) => {
  currentPrimaryUnit.value = unit
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteUnit${unit.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранного юнита из репорта и закрыть окно
const cancelRemovePrimaryUnit = () => {
  confirmationModal.hide();
  currentPrimaryUnit.value = {};
}

// Подтвердить и отправить запрос на удаление выбранного юнита из репорта
// Запросить обновлённый список тем из репорта и заменить переменную в reportStore
const removePrimaryUnit = () => {
  // console.log('Запрос на удаление достижения по теме: ', currentPrimaryTopic.value);
  reportStore.removeReportMentorPrimaryUnit(currentPrimaryUnit.value.id).then(() => {
    authStore.showMessageSuccess('Достижения в исследовательской деятельности удалены');
    getReportPrimaryUnits();
  })
  confirmationModal.hide();
}

// Функция редактирования конкретного поля в юните
const handleSave = async (editData, id) => {
  console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для юнита с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  reportStore.updateReportMentorPrimaryUnit(updatingData).then((result) => {
    // console.log('Результаты прохождения учебных тем успешно обновлены: ', result);
    // Перезапись отредактированного объекта в report
    authStore.showMessageSuccess('Достижения в исследовательской деятельности успешно записаны');
    const index = reportStore.studentMentorReports.findIndex(item => item.report.id === props.report.id);
    if (index != -1) {
      reportStore.studentMentorReports[index].report.pyp_units = reportStore.studentMentorReports[index].report.pyp_units.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  })
};


const getReportPrimaryUnits = () => {
  const config = {
    params: {
      report: props.report.id
    }
  }
  reportStore.loadReportMentorPrimaryUnits(config).then((result) => {
    const index = reportStore.studentMentorReports.findIndex(
      (item) => item.report.id === props.report.id
    );
    reportStore.studentMentorReports[index].report.pyp_units = [...result.data];
  })
}

</script>