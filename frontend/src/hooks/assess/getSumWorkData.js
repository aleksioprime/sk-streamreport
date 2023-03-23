import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getSumWork() {
	const sumWorks = ref([]);
	const getSumWorkData = async (data) => {
		const config = {
			params: {
				teacher: data.teacher || "",
				period: data.period || "",
			}
		}
		await axiosAPI.get('/assessment/sumwork', config).then((response) => {
			console.log("Загрузка итоговых работ")
			sumWorks.value = response.data;
			console.log(sumWorks.value)
		});
	};
	return {
		sumWorks, getSumWorkData
	}
}

export function getTeachers() {
	const teachers = ref([]);
	const getTeachersData = async () => {
		await axiosAPI.get('/teachers').then((response) => {
			teachers.value = response.data;
			// console.log(teachers.value)
		});
	};
	return {
		teachers, getTeachersData
	}
}

export function getGrades() {
	const grades = ref([]);
	const getGradesData = async (program) => {
		const config = {
			params: {
				program: program
			}
		}
		await axiosAPI.get('/grades', config).then((response) => {
			grades.value = response.data;
		});
	};
	return {
		grades, getGradesData
	}
}

export function getSubjects() {
	const subjects = ref([]);
	const getSubjectsData = async (level, type) => {
		const config = {
			params: {
				level: level,
				type: type,
			}
		}
		await axiosAPI.get('/subjects', config).then((response) => {
			subjects.value = response.data;
		});
	};
	return {
		subjects, getSubjectsData
	}
}

export function getPeriods() {
	const periods = ref([]);
	const currentPeriod = ref({});
	const getPeriodsData = async (study_year) => {
		const config = {
			params: {
				study_year: study_year,
			}
		}
		await axiosAPI.get('/assessment/period', config).then((response) => {
			periods.value = response.data;
			console.log("Получение периодов обучения: ", periods.value)
			currentPeriod.value = periods.value.find((item) => {
				const currentDate = new Date();
				const startDate = new Date(item.date_start);
				const endDate = new Date(item.date_end);
				// console.log(currentDate, startDate, endDate);
				return currentDate > startDate && currentDate < endDate;
			  })
			  console.log("Текущие период: ", currentPeriod.value)
		});
	};
	return {
		periods, currentPeriod, getPeriodsData
	}
}

export function getStudyYears() {
	const studyYears = ref([]);
	const currentStudyYear = ref({});
	const getStudyYearsData = async () => {
		await axiosAPI.get('/assessment/year').then((response) => {
			studyYears.value = response.data;
			console.log("Получение учебных лет: ", studyYears.value)
			currentStudyYear.value = studyYears.value.find((item) => {
				const currentDate = new Date();
				const startDate = new Date(item.date_start);
				const endDate = new Date(item.date_end);
				// console.log(new Date(), item.date_start, item.date_end);
				return currentDate > startDate && currentDate < endDate;
			  })
			  console.log("Текущий год: ", currentStudyYear.value)
		});
	};
	return {
		studyYears, currentStudyYear, getStudyYearsData
	}
}