<template>
  <div>
    <div class="d-flex align-items-center mb-2">
      <h5>Академические достижения</h5>
      <div class="ms-auto">
        <i class="bi bi-three-dots dots dot-menu" data-bs-toggle="dropdown" aria-expanded="false"></i>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="##" @click="showTopicImportModal(report)">Добавить темы</a></li>
        </ul>
      </div>
    </div>
    <table class="table table-sm table-bordered" v-if="report.topic_achievements.length">
      <thead>
        <tr>
          <th scope="col" style="width: 40%;">Тема</th>
          <th scope="col" style="min-width: 120px;">Достижение</th>
          <th scope="col" style="width: 60%;">Комментарий</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="achieve in report.topic_achievements" :key="achieve.id">
          <td>
            <span class="me-2">{{ achieve.topic.name }}</span>
            <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(achieve)"></i>
            <confirmation-modal v-if="achieve.id == currentPrimaryTopic.id" :nameModal="`confirmationDeleteTopic${achieve.id}`" @confirm="removePrimaryTopic"
              @cancel="cancelRemovePrimaryTopic">
              Вы действитель хотите удалить эту тему?
            </confirmation-modal>
          </td>
          <td>
            <editable-dropdown-cell :propData="achieve.level" :propItems="reportStore.levels" 
            showName="name" propName="level" saveName="value" @save="handleSave($event, achieve.id)" />
          </td>
          <td>
            <editable-textarea-cell :propData="achieve.comment" propName="comment" @save="handleSave($event, achieve.id)" />
          </td>
        </tr>
      </tbody>
    </table>
    <div class="card" v-else>
      <div class="card-body">
        <div class="d-flex justify-content-center">
          Академических достижений пока нет
        </div>
      </div>
    </div>
    <simple-modal v-if="report.id == currentReport.id" :nameModal="`topicImportModal${report.id}`"
      titleConfirm="Добавить темы" titleModal="Добавление предметных тем в репорт студента"
      @confirm="confirmTopicImportModal" @cancel="cancelTopicImportModal">
      <div>
        <div v-if="syllabusStore.courses.length">
          <div v-for="course in syllabusStore.courses" :key="course.id">
            <h5>{{ course.syllabus.subject.name }} ({{ course.year.number }} класс)</h5>
            <div v-for="chapter in course.chapters" :key="chapter.id">
              <div class="my-2">
                <strong>Раздел: {{ chapter.name }}</strong>
                <a href="##" @click="selectChapterTopics(chapter)" class="mx-2">Выделить всё</a>
                <a href="##" @click="unSelectChapterTopics(chapter)" class="mx-2">Снять выделение</a>
              </div>
              <div class="form-check" v-for="topic in chapter.topics" :key="topic.id">
                <input class="form-check-input" type="checkbox" :value="topic.id" :id="`check-${topic.id}`"
                  v-model="choiceTopics" :disabled="checkDisableTopic(topic.id)">
                <label class="form-check-label" :for="`check-${topic.id}`">
                  {{ topic.name }}
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </simple-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import EditableTextareaCell from "@/common/components/EditableTextareaCell.vue";
import EditableDropdownCell from "@/common/components/EditableDropdownCell.vue";
import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import SimpleModal from '@/common/components/SimpleModal.vue';
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";
import { useSyllabusStore } from "@/stores/syllabus";

const props = defineProps({
  report: {
    type: Object,
    default: {}
  },
});

const authStore = useAuthStore();
const reportStore = useReportStore();
const syllabusStore = useSyllabusStore();

let confirmationModal = null
let topicImportModal = null

const currentPrimaryTopic = ref({})
const currentReport = ref({})
const choiceTopics = ref([])

// Условие отключения чекбокса для темы, которая уже была добавлена в репорт
const checkDisableTopic = (id) => {
  return props.report.topic_achievements.some(item => item.topic.id == id)
}

// ************ Модальное окно для добавления тем курса в репорт ************

// Создать и показать модальное окно для добавления в репорт выделенных тем
// Сделать запрос на вывод в модальное окно курсов текущего предмета и года
const showTopicImportModal = (report) => {
  currentReport.value = report
  nextTick(() => {
    topicImportModal = new Modal(`#topicImportModal${report.id}`, { backdrop: 'static' });
    topicImportModal.show();
  });
  syllabusStore.loadCourses({
    params: {
      year: report.group.year_study.id,
      syllabus__subject: report.subject.id
    } 
  })
}

// Отменить добавление в репорт тем курса и закрыть модальное окно
const cancelTopicImportModal = () => {
  topicImportModal.hide();
  choiceTopics.value = [];
  currentReport.value = {};
}

// Подтвердить и отправить запрос на добавление выбранных тем в репорт студента
// Запросить обновлённый список тем из репорта и заменить переменную в reportStore
const confirmTopicImportModal = () => {
  // console.log('Добавление тем в репорт студента: ', choiceTopics.value)
  topicImportModal.hide();
  const creatingData = choiceTopics.value.map(number => ({
    topic: number,
    report: props.report.id
  }));
  reportStore.createReportPrimaryTopic(creatingData).then((result) => {
    getReportPrimaryTopics();
  })
  choiceTopics.value = [];
  currentReport.value = {};
}

// Выделить все активные темы для добавления в репорт
const selectChapterTopics = (chapter) => {
  choiceTopics.value = chapter.topics.filter(item => !props.report.topic_achievements.map(i => i.topic.id).includes(item.id)).map(item => item.id)
}

// Снять выделение всех тем
const unSelectChapterTopics = (chapter) => {
  choiceTopics.value = choiceTopics.value.filter(item => !chapter.topics.map(i => i.id).includes(item));
}

// ************ Модальное окно для удаления выбранной темы из репорта ************

// Открыть модальное окно для подтверждения удаления выбранной темы из репорта
const showConfirmationModal = (achieve) => {
  currentPrimaryTopic.value = achieve
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteTopic${achieve.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной темы из репорта и закрыть окно
const cancelRemovePrimaryTopic = () => {
  confirmationModal.hide();
  currentPrimaryTopic.value = {};
}

// Подтвердить и отправить запрос на удаление выбранной темы из репорта
// Запросить обновлённый список тем из репорта и заменить переменную в reportStore
const removePrimaryTopic = () => {
  // console.log('Запрос на удаление достижения по теме: ', currentPrimaryTopic.value);
  reportStore.removeReportPrimaryTopic(currentPrimaryTopic.value.id).then(() => {
    getReportPrimaryTopics();
  })
  confirmationModal.hide();
}

// Функция редактирования конкретного поля в достижении по учебной теме
const handleSave = async (editData, id) => {
  // console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  reportStore.updateReportPrimaryTopic(updatingData).then((result) => {
    // console.log('Результаты прохождения учебных тем успешно обновлены: ', result);
    // Перезапись отредактированного объекта в report
    authStore.showMessageSuccess(`Академические успехи студента ${props.report.student.short_name} успешно сохранены!`);
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    if (index != -1) {
      reportStore.reportTeachers[index].topic_achievements = reportStore.reportTeachers[index].topic_achievements.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  })
};

// Функция запроса достижений по учебным темам конкретного репорта и замена этого блока в переменной reportStore
const getReportPrimaryTopics = () => {
  const config = {
    params: {
      report: props.report.id
    }
  }
  reportStore.loadReportPrimaryTopics(config).then((result) => {
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    reportStore.reportTeachers[index].topic_achievements = [...result.data]
  })
}

onMounted(() => {
  
})
</script>

<style>

.dots {
  font-size: 1.2rem;
}
</style>