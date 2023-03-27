import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getSumWork() {
	const sumWork = ref({
		criteria: []
	});
	const getSumWorkData = async (id_sumwork, callback) => {
		await axiosAPI.get(`/assessment/sumwork/${id_sumwork}`).then((response) => {
			console.log("Загрузка итоговой работы")
			sumWork.value = response.data;
			console.log(sumWork.value)
			callback();
		});
	};
	return {
		sumWork, getSumWorkData
	}
}

export function getStudents() {
	const students = ref([]);
	const getStudentsData = async (data) => {
		const config = {
			params: {
				class: data.class || "",
			}
		}
		await axiosAPI.get('/student', config).then((response) => {
			students.value = response.data;
			console.log("Студенты: ", students.value)
		});
	};
	return {
		students, getStudentsData
	}
}

export function getWorkAssess() {
	const workAssess = ref([]);
	const getWorkAssessData = async (group, callback) => {
    const config = {
			params: {
				class: group,
			}
		}
		await axiosAPI.get(`/assessment/workassess`, config).then((response) => {
			console.log("Загрузка оценок за итоговые работы")
			workAssess.value = response.data;
			console.log(workAssess.value)
			callback();
		});
	};
	return {
		workAssess, getWorkAssessData
	}
}