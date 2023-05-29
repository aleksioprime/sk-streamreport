import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getClassYears() {
  const years = ref([]);
  const fetchGetClassYears = async (data) => {
    const config = {
      params: {
        program: data.program || null,
        subject: data.subject || null,
        department: data.department || null,
        author: data.author || null,
        teacher: data.teacher || null,
        level: data.level || null,
      }
    }
    await axiosAPI.get('myp/years', config).then((response) => {
        years.value = response.data;
    });
  };
  return {
    years, fetchGetClassYears
  }
}
