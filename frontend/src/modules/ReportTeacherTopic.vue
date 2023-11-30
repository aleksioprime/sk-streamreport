<template>
  <div>
    <table class="table table-sm table-bordered">
      <thead>
        <tr>
          <th scope="col" class="w-50">Тема</th>
          <th scope="col" style="width: 100px;">Достижение</th>
          <th scope="col" class="w-50">Комментарий</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="achieve in report.topic_achievements" :key="achieve.id">
          <td>{{ achieve.topic.name }}</td>
          <td>{{ achieve.level }}</td>
          <td>
            <editable-cell :propData="achieve.comment" propName="comment" @save="handleSave($event, achieve.id)"/>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import EditableCell from "@/common/components/EditableCell.vue";
import { useReportStore } from "@/stores/report";
import { useAuthStore } from "@/stores/auth";

const props = defineProps({
  report: {
    type: Object,
    default: {}
  },
});

const authStore = useAuthStore();
const reportStore = useReportStore();

const handleSave = async (editData, id) => {
  console.log(`Сохраняемое значение для ${editData.propName}: ${editData.value} для репорта с ID: ${id}`);
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  reportStore.updateReportPrimaryTopic(updatingData).then((result) => {
      console.log('Результаты прохождения учебных тем успешно обновлены: ', result);
      // Перезапись отредактированного объекта в report
      authStore.showMessageSuccess();
      const index = reportStore.reportTeachersPrimary.findIndex(item => item.id === props.report.id);
      if (index != -1) {
        reportStore.reportTeachersPrimary[index].topic_achievements = reportStore.reportTeachersPrimary[index].topic_achievements.map(item => item.id === result.data.id ? { ...result.data } : item);
      }
    })
};

</script>