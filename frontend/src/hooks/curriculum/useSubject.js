import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getSubjects() {
  const subjects = ref([]);
  const fetchGetSubjects = async (data) => {
    const config = {
      params: {
        department: data.department || null,
        level: data.level || null,
        type: data.type || null,
        teacher: data.teacher || null,
        program: data.program || null,
      }
    }
    await axiosAPI.get('myp/subjects', config).then((response) => {
        console.log('Получен список предметов: ', response.data)
        subjects.value = response.data;
    });
  };
  return {
    subjects, fetchGetSubjects
  }
}
