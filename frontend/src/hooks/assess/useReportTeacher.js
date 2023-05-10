import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getStudentsReport() {
  const studentsReport = ref([]);
  const isStudentsReportLoading = ref(true);
  const fetchGetStudentsReport = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        subject: data.subject || null,
        study_year: data.study_year || null,
      }
    }
    isStudentsReportLoading.value = true;
    await axiosAPI.get('/assessment/student/report/teacher', config).then((response) => {
      console.log('Получен список студентов для репорта: ', response.data)
      studentsReport.value = response.data;
    }).finally(() => {
      isStudentsReportLoading.value = false;
    });
  };
  return {
    studentsReport, isStudentsReportLoading, fetchGetStudentsReport
  }
}

export function createReportTeacher() {
  const createdReportTeacher = ref([]);
  const fetchCreateReportTeacher = async (data) => {
    await axiosAPI.post('/assessment/report/teacher', data).then((response) => {
      console.log('Репорт успешно создан: ', response.data)
      createdReportTeacher.value = response.data;
    });
  };
  return {
    createdReportTeacher, fetchCreateReportTeacher
  }
}

export function updateReportTeacher() {
  const updatedReportTeacher = ref([]);
  const fetchUpdateReportTeacher = async (data) => {
    await axiosAPI.put(`/assessment/report/teacher/${data.id}`, data).then((response) => {
      console.log('Репорт успешно обновлён: ', response.data)
      updatedReportTeacher.value = response.data;
    });
  };
  return {
    updatedReportTeacher, fetchUpdateReportTeacher
  }
}