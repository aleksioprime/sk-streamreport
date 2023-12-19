<template>
  <div>
    <div class="my-2">
      <h5>IB Learner Profile</h5>
      <div v-for="profile in filteredlearnerProfiles" :key="profile.id" class="d-flex align-items-center my-2">
        <div class="me-3" :class="{ 'selected-profile': profile.report }">{{ profile.name }}</div>
        <div class="ms-auto">
          <div v-if="profile.report" >
            <editable-dropdown-cell :propData="profile.report.level" :propItems="PROFILE_LEVELS" 
            showName="name" propName="level" saveName="value" @save="handleSave($event, profile.report.id)" 
            :disabled="!allowedMode"/>
          </div>
          <div v-else>Профиль не оценивается</div>
        </div>
        <div v-if="allowedMode">
          <i class="bi bi-dash-square dot-menu ms-2" v-if="profile.report"
          @click="removeReportMentorIbProfile(profile.report.id)"></i>
          <i v-else class="bi bi-plus-square dot-menu ms-2" @click="createReportMentorIbProfile(profile.id)"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useIboStore } from "@/stores/ibo";
import { useReportStore } from "@/stores/report";
import { PROFILE_LEVELS } from "@/common/constants";
import EditableDropdownCell from "@/common/components/EditableDropdownCell.vue";

const props = defineProps({
  report: {
    type: Object,
    default: {},
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const emit = defineEmits(["save"]);

const iboStore = useIboStore();
const reportStore = useReportStore();

// Добавление в объекты профилей свойства report с данными о добавленных IB Learner Profile
const filteredlearnerProfiles = computed(() => {
  return iboStore.learnerProfiles
    .map((item) => {
      return {
        ...item,
        report: props.report.profiles.find(
          (i) => i.profile.id == item.id
        ),
      };
    });
});

// Функция редактирования конкретного поля и обновление данных из результата
const handleSave = async (editData, id) => {
  console.log(
    `Сохраняемое значение для ${editData.propName}: ${editData.value} для записи с ID: ${id}`
  );
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  reportStore.updateReportMentorIbProfile(updatingData).then((result) => {
    authStore.showMessageSuccess('Сохранено');
    const index = reportStore.studentMentorReports.findIndex(item => item.report.id === props.report.id);
    if (index != -1) {
      reportStore.studentMentorReports[index].report.profiles = reportStore.studentMentorReports[index].report.profiles.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  });
};

// Функция запроса на создание оценки профиля в репорте
const createReportMentorIbProfile = (id) => {
  const data = {
    report: props.report.id,
    profile: id,
  };
  reportStore.createReportMentorIbProfile(data).then((result) => {
    authStore.showMessageSuccess('Профиль IB-студента для оценки добавлен');
    getReportMentorIbProfiles();
  });
};

// Функция запроса на удаление выбранного достижения профиля из репорта
const removeReportMentorIbProfile = (id) => {
  reportStore.removeReportMentorIbProfile(id).then(() => {
    authStore.showMessageSuccess('Профиль IB-студента для оценки удалён');
    getReportMentorIbProfiles();
  });
};

// Функция запроса достижений по профилю конкретного репорта и замена этого блока в переменной reportStore
// Выполняется после добавления или удаления критерия из репорта
const getReportMentorIbProfiles = () => {
  const config = {
    params: {
      report: props.report.id,
    },
  };
  reportStore.loadReportMentorIbProfiles(config).then((result) => {
    const index = reportStore.studentMentorReports.findIndex(
      (item) => item.report.id === props.report.id
    );
    reportStore.studentMentorReports[index].report.profiles = [ ...result.data ];
  });
};

onMounted(() => { });
</script>

<style scoped>
.selected-profile {
  font-size: 1.1rem;
  font-weight: 500;
}
</style>