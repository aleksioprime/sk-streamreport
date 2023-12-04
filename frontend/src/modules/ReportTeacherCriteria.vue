<template>
  <div>
    <div class="d-flex align-items-center mb-2">
      <h5>Достижения по критериям Гимназии</h5>
      <div class="ms-auto">
        <i class="bi bi-three-dots dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="##" @click="showCriterionImportModal(report)">Добавить критерии</a></li>
        </ul>
      </div>
    </div>
    <div v-if="report.criterion_achievements.length">
      <table class="table table-sm table-bordered">
      <thead>
        <tr>
          <th scope="col" style="width: 100%;">Критерий</th>
          <th scope="col" style="min-width: 120px;">Результат</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="achievement in report.criterion_achievements" :key="achievement.id">
          <td>
            <span class="me-2">{{ achievement.criterion.name }}</span>
            <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(achievement)"></i>
            <confirmation-modal v-if="achievement.id == currentTeacherCriterion.id" :nameModal="`confirmationDeleteCriterion${achievement.id}`" @confirm="removeTeacherCriterion"
              @cancel="cancelRemoveTeacherCriterion">
              Вы действитель хотите удалить этот критерий?
            </confirmation-modal>
          </td>
          <td>
            <editable-dropdown-cell :propData="achievement.achievement" :propItems="achievement.criterion.levels" 
            showName="name" propName="achievement" title="Выберите уровень" saveName="id" @save="handleSave($event, achievement.id)" />
          </td>
        </tr>
      </tbody>
    </table>
    </div>
    <div class="card" v-else>
      <div class="card-body">
        <div class="d-flex justify-content-center">
          Оценки по критериям пока нет
        </div>
      </div>
    </div>
    <simple-modal v-if="report.id == currentReport.id" :nameModal="`criterionImportModal${report.id}`"
      titleConfirm="Добавить критерии" titleModal="Добавление критериев в репорт студента"
      @confirm="confirmCriterionImportModal" @cancel="cancelCriterionImportModal">
      <div>
        <div>
          <div class="my-2">
            <h5>Общие критерии</h5>
            <div v-if="groupedCriteria.withoutSubjects && groupedCriteria.withoutSubjects.length">
              <div class="form-check" v-for="criterion in groupedCriteria.withoutSubjects" :key="criterion.id">
                <input class="form-check-input" type="checkbox" :value="criterion.id" :id="`check-${criterion.id}`"
                  v-model="choiceCriteria" :disabled="checkDisableCriterion(criterion.id)">
                <label class="form-check-label" :for="`check-${criterion.id}`">
                  {{ criterion.name }} (<span v-for="level, index in criterion.levels" :key="level.id">{{ level.name }}<span v-if="index+1 != criterion.levels.length">, </span></span>)
                </label>
              </div>
            </div>
            <div v-else class="my-2">Критериев не найдено</div>
          </div>
          <div class="my-2">
            <h5>Предметные критерии</h5>
            <div v-if="groupedCriteria.withoutSubjects && groupedCriteria.withoutSubjects.length">
              <div class="form-check" v-for="criterion in groupedCriteria.withSubjects" :key="criterion.id">
                <input class="form-check-input" type="checkbox" :value="criterion.id" :id="`check-${criterion.id}`"
                  v-model="choiceCriteria" :disabled="checkDisableCriterion(criterion.id)">
                <label class="form-check-label" :for="`check-${criterion.id}`">
                  {{ criterion.name }} (<span v-for="level, index in criterion.levels" :key="level.id">{{ level.name }}<span v-if="index+1 != criterion.levels.length">, </span></span>)
                </label>
              </div>
            </div>
            <div v-else class="my-2">Критериев не найдено</div>
          </div>
      </div>
      </div>
    </simple-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import SimpleModal from '@/common/components/SimpleModal.vue';
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import EditableDropdownCell from "@/common/components/EditableDropdownCell.vue";

import { useAuthStore } from "@/stores/auth";
import { useReportStore } from "@/stores/report";

const props = defineProps({
  report: {
    type: Object,
    default: {}
  },
});

const authStore = useAuthStore();
const reportStore = useReportStore();

let criterionImportModal = null
let confirmationModal = null

const currentReport = ref({})
const currentTeacherCriterion = ref({})
const choiceCriteria = ref([])

// Условие отключения чекбокса для критерия, который уже была добавлена в репорт
const checkDisableCriterion = (id) => {
  return props.report.criterion_achievements.some(item => item.criterion.id == id)
}

// Группировка критериев по наличию предметов
const groupBySubjects = (arr) => {
  return arr.reduce((accumulator, obj) => {
    // Проверяем, существует ли свойство 'subjects' и является ли оно непустым массивом
    let key = Array.isArray(obj.subjects) && obj.subjects.length > 0 ? 'withSubjects' : 'withoutSubjects';

    // Инициализируем ключ в аккумуляторе, если это необходимо
    if (!accumulator[key]) {
      accumulator[key] = [];
    }

    // Добавляем объект в соответствующую группу
    accumulator[key].push(obj);

    return accumulator;
  }, {});
}

// Фильтр списка классов по выбранному учебному плану
const groupedCriteria = computed(() => {
  return groupBySubjects(reportStore.reportCriteria)
});

// ************ Модальное окно для добавления критериев в репорт ************

// Запрос на получение критериев по году и предмету
const getReportCriteria = () => {
  let config = {
    params: {
      years: props.report.group.year_study.id,
      subjects: props.report.subject.id,
    }
  }
  reportStore.loadReportCriteria(config);
}

// Создать и показать модальное окно для добавления в репорт выделенных критериев
// Сделать запрос на вывод в модальное окно критериев
const showCriterionImportModal = (report) => {
  currentReport.value = report
  nextTick(() => {
    criterionImportModal = new Modal(`#criterionImportModal${report.id}`, { backdrop: 'static' });
    criterionImportModal.show();
  });
  getReportCriteria();
}

// Отменить добавление в репорт тем курса и закрыть модальное окно
const cancelCriterionImportModal = () => {
  criterionImportModal.hide();
  choiceCriteria.value = [];
  currentReport.value = {};
}

// Подтвердить и отправить запрос на добавление выбранных критериев в репорт студента
// Запросить обновлённый список критериев из репорта и заменить переменную в reportStore
const confirmCriterionImportModal = () => {
  // console.log('Импорт критерив в репорт студента: ', choiceCriteria.value)
  criterionImportModal.hide();
  const creatingData = choiceCriteria.value.map(number => ({
    criterion: number,
    report: props.report.id
  }));
  reportStore.createReportTeacherAchievement(creatingData).then((result) => {
    // console.log(result)
    getReportTeacherAchievements();
  })
  choiceCriteria.value = [];
  currentReport.value = {};
}

// Функция запроса достижений по критериям конкретного репорта и замена этого блока в переменной reportStore
const getReportTeacherAchievements = () => {
  const config = {
    params: {
      report: props.report.id
    }
  }
  reportStore.loadReportTeacherAchievements(config).then((result) => {
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    reportStore.reportTeachers[index].criterion_achievements = [...result.data]
  })
}

// ************ Модальное окно для удаления выбранного критерия из репорта ************

// Открыть модальное окно для подтверждения удаления выбранного критерия из репорта
const showConfirmationModal = (achievement) => {
  currentTeacherCriterion.value = achievement
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteCriterion${achievement.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранного критерия из репорта и закрыть окно
const cancelRemoveTeacherCriterion = () => {
  confirmationModal.hide();
  currentTeacherCriterion.value = {};
}

// Подтвердить и отправить запрос на удаление выбранного критерия из репорта
// Запросить обновлённый список критериев из репорта и заменить переменную в reportStore
const removeTeacherCriterion = () => {
  // console.log('Запрос на удаление достижения по теме: ', currentTeacherCriterion.value);
  reportStore.removeReportTeacherAchievement(currentTeacherCriterion.value.id).then(() => {
    getReportTeacherAchievements();
  })
  confirmationModal.hide();
}

// Функция редактирования конкретного поля в результатах по критериям
const handleSave = async (editData, id) => {
  // console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  reportStore.updateReportTeacherAchievement(updatingData).then((result) => {
    // console.log('Результаты критерия успешно обновлены: ', result);
    // Перезапись отредактированного объекта в report
    authStore.showMessageSuccess(`Результаты по критерию у студента ${props.report.student.short_name} успешно сохранены!`);
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    if (index != -1) {
      reportStore.reportTeachers[index].criterion_achievements = reportStore.reportTeachers[index].criterion_achievements.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  })
};
</script>