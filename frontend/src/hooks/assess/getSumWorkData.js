import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getSumWork() {
	const sumWorks = ref([]);
	const getSumWorkData = async (teacher) => {
		const config = {
			params: {
				teacher: teacher,
			}
		}
		await axiosAPI.get('/assessment/sumwork', config).then((response) => {
			console.log("Загрузка итоговых работ")
			sumWorks.value = response.data;
		});
	};
	return {
		sumWorks, getSumWorkData
	}
}