<template>
  <div>
    <div class="my-2">
      <h5>Предметные критерии</h5>
      <div class="my-3">
        <div v-for="criterion in filteredCriteriaMyp" :key="criterion.id" class="d-flex align-items-center my-2">
          <div class="me-3" :class="{ 'selected-criterion': criterion.report }">{{ criterion.letter.toUpperCase() }}. {{
            criterion.name }}</div>
          <i class="bi bi-dash-square dot-menu me-2" v-if="criterion.report"
            @click="removeReportSecondaryCriterion(criterion.report.id)"></i>
          <i v-else class="bi bi-plus-square dot-menu me-2" @click="createReportSecondaryCriterion(criterion.id)"></i>
          <div class="ms-auto">
            <scale-radio :elementId="String(report.id) + String(criterion.id)" :data="MARK8"
              :propValue="criterion.report.mark" propName="mark" @save="handleSave($event, criterion.report.id)"
              v-if="criterion.report" />
            <div v-else>Критерий не оценивается</div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import ScaleRadio from "@/common/components/ScaleRadio.vue";
import { useUnitMypStore } from "@/stores/unitMyp";
import { useReportStore } from "@/stores/report";
import { MARK8 } from "@/common/constants";

const props = defineProps({
  report: {
    type: Object,
    default: {},
  },
});

const reportStore = useReportStore();
const unitMypStore = useUnitMypStore();
const emit = defineEmits(["save"]);

// Фильтр списка MYP критериев по предмету репорта, а также добавление свойства report с данными о добавленных критериях
const filteredCriteriaMyp = computed(() => {
  return unitMypStore.objectives
    .filter((item) => {
      return item.group.id == props.report.subject.group_ib;
    })
    .map((item) => {
      return {
        ...item,
        report: props.report.criterion_marks.find(
          (i) => i.criterion.id == item.id
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
  reportStore.updateReportSecondaryCriterion(updatingData).then((result) => {
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    if (index != -1) {
      reportStore.reportTeachers[index].criterion_marks = reportStore.reportTeachers[index].criterion_marks.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  });
};

const createReportSecondaryCriterion = (id) => {
  const data = {
    report: props.report.id,
    criterion: id,
  };
  reportStore.createReportSecondaryCriterion(data).then((result) => {
    getReportSecondaryCriteria();
  });
};

// Функция запроса на удаление выбранного критерия из оценки репорта
const removeReportSecondaryCriterion = (id) => {
  reportStore.removeReportSecondaryCriterion(id).then(() => {
    getReportSecondaryCriteria();
  });
};

// Функция запроса оценок по критериям конкретного репорта и замена этого блока в переменной reportStore
// Выполняется после добавления или удаления критерия из репорта
const getReportSecondaryCriteria = () => {
  const config = {
    params: {
      report: props.report.id,
    },
  };
  reportStore.loadReportSecondaryCriteria(config).then((result) => {
    const index = reportStore.reportTeachers.findIndex(
      (item) => item.id === props.report.id
    );
    reportStore.reportTeachers[index].criterion_marks = [...result.data];
  });
};

onMounted(() => { });
</script>

<style scoped>
.selected-criterion {
  font-size: 1.1rem;
  font-weight: 500;
}
</style>