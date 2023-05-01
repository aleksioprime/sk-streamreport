import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getCriteriaMYP() {
  const criteriaMYP = ref([]);
  const fetchGetCriteriaMYP = async (data) => {
    const config = {
      params: {
        subject: data.subject || null
      }
    }
    await axiosAPI.get('myp/criteria', config).then((response) => {
      criteriaMYP.value = response.data;
    });
  };
  return {
    criteriaMYP, fetchGetCriteriaMYP
  }
}
