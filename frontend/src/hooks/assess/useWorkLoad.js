import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getWorkLoads() {
	const workLoads = ref([]);
	const fetchGetWorkLoads = async (data) => {
        const config = {
			params: {
				teacher: data.teacher || null,
                study_year: data.study_year || null,
			}
		}
		await axiosAPI.get('/assessment/workload', config).then((response) => {
			workLoads.value = response.data;
			console.log("Получение нагрузки учителя: ", workLoads.value)
		});
	};
	return {
		workLoads, fetchGetWorkLoads
	}
}
