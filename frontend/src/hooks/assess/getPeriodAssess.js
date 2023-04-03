import { ref, onMounted, computed } from 'vue'
import { axiosAPI } from '@/axios'

export function getPeriodAssess() {
	const periodAssess = ref([]);
	const getPeriodAssessData = async (data) => {
		const config = {
			params: {
				student: data.student || null,
				period: data.period || null,
				subject: data.subject || null,
				year: data.year || null,
			}
		}
		await axiosAPI.get(`/assessment/periodassess`).then((response) => {
			console.log("Загрузка оценок за период")
			periodAssess.value = response.data;
			console.log(periodAssess.value)
		});
	};
	return {
		periodAssess, getPeriodAssessData
	}
}

export function getStudents() {
	const students = ref([]);
	const getStudentsData = async (data) => {
		const config = {
			params: {
				year: data.year || null,
				period: data.period || null,
				subject: data.subject || null,
			}
		}
		console.log(config)
		await axiosAPI.get('/assessment/student', config).then((response) => {
			students.value = response.data;
			console.log("Студенты: ", students.value)
		});
	};
	return {
		students, getStudentsData
	}
}

export function getSumWork() {
	const sumWorks = ref([]);
	const getSumWorkData = async (data) => {
		const config = {
			params: {
				teacher: data.teacher || null,
				period: data.period || null,
				year: data.year || null,
				subject: data.subject || null,
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

export function getGroupedArray() {
	function groupedArrayData (array, fields) {
		let groupedObject = array.reduce((acc, obj) => {
		  let objField = obj
		  for (const field of fields) {
			objField = objField[field];
		  }
		  const property = objField.id;
		  acc[property] = acc[property] || [];
		  acc[property].push(obj);
		  return acc;
		}, {});
		return groupedObject;
	  }
	return  {
		groupedArrayData
	}
}

export function getAssessmentJournal() {
	const currentPeriod = ref({});
	const currentYear = ref({});
	const currentSubject = ref({group_ib: {}});
	const currentGroups = ref([]);
	const getAssssmentJournalData = async (data) => {
		const config = {
			params: {
				period: data.period || null,
				year: data.year || null,
				subject: data.subject || null,
			}
		}
		await axiosAPI.get('/assessment/journal', config).then((response) => {
			console.log("Загрузка данных для журнала")
			currentPeriod.value = response.data.period;
			currentYear.value = response.data.year;
			currentSubject.value = response.data.subject;
			currentGroups.value = response.data.groups;
			console.log(response.data)
		});
	};
	return {
		currentPeriod, currentYear, currentSubject, currentGroups, getAssssmentJournalData
	}
}

export function filterStudentsByGroup(students) {
    const queryGroup = ref(null);
    const filteredStudentsByGroup = computed(() => {
		if (queryGroup.value) {
        	return students.value.filter(item => queryGroup.value == item.group.id);
		} else {
			return students.value
		}
    });
    return {
        queryGroup, filteredStudentsByGroup
    }
};