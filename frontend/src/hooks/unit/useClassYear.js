import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getClassYears() {
  const years = ref([]);
  const fetchGetClassYears = async (data) => {
    const config = {
      params: {
        program: data.program || null,
        subject: data.subject || null,
        teacher: data.teacher || null
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
