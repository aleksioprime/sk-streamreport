import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getReportMentorJournal() {
  const currentReportPeriod = ref({});
  const subjects = ref([]);
  const currentGroup = ref({ mentor: { user: {} }, class_year: {} });  const eventTypes = ref([]);
  const fetchGetReportMentorJournal = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        group: data.group || null,
      }
    }
    await axiosAPI.get('assessment/report/mentor/journal', config).then((response) => {
      console.log("Загрузка данных для журнала")
      currentReportPeriod.value = response.data.period;
      currentGroup.value = response.data.group;
      subjects.value = response.data.subjects;
      eventTypes.value = response.data.event_types
      console.log(response.data)
    });
  };
  return {
    currentGroup, subjects, currentReportPeriod, eventTypes, fetchGetReportMentorJournal
  }
}

export function getStudentsReport() {
  const studentsReport = ref([]);
  const isStudentsReportLoading = ref(true);
  const fetchGetStudentsReport = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        study_year: data.study_year || null,
      }
    }
    isStudentsReportLoading.value = true;
    await axiosAPI.get('/assessment/student/report/mentor', config).then((response) => {
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

export function getStudentReport() {
  const studentReport = ref({});
  const isStudentReportLoading = ref(false);
  const fetchGetStudentReport = async (id, data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        study_year: data.study_year || null,
      }
    }
    isStudentReportLoading.value = true;
    await axiosAPI.get(`/assessment/student/report/mentor/${id}`, config).then((response) => {
      console.log('Получен студент для репорта: ', response.data)
      studentReport.value = response.data;
    }).finally(() => {
      isStudentReportLoading.value = false;
    });
  };
  return {
    studentReport, fetchGetStudentReport
  }
}

export function createReportMentor() {
  const createdReportMentor = ref([]);
  const fetchCreateReportMentor = async (data) => {
    await axiosAPI.post('/assessment/report/mentor', data).then((response) => {
      console.log('Репорт успешно создан: ', response.data)
      createdReportMentor.value = response.data;
    });
  };
  return {
    createdReportMentor, fetchCreateReportMentor
  }
}

export function updateReportMentor() {
  const updatedReportMentor = ref([]);
  const fetchUpdateReportMentor = async (data) => {
    await axiosAPI.put(`/assessment/report/mentor/${data.id}`, data).then((response) => {
      console.log('Репорт успешно обновлён: ', response.data)
      updatedReportMentor.value = response.data;
    });
  };
  return {
    updatedReportMentor, fetchUpdateReportMentor
  }
}