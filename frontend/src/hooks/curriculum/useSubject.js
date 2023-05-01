import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getSubjects() {
  const subjects = ref([]);
  const fetchGetSubjects = async (data) => {
    const config = {
      params: {
        level: data.level || null,
        type: data.type || null,
        teacher: data.teacher || null,
      }
    }
    await axiosAPI.get('myp/subjects', config).then((response) => {
        subjects.value = response.data;
    });
  };
  return {
    subjects, fetchGetSubjects
  }
}
