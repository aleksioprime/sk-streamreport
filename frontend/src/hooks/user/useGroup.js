import { ref, onMounted } from 'vue'
import { axiosAPI } from '@/axios'

export function getGroups() {
  const groups = ref([]);
  const isGroupLoading = ref(true)
  const fetchGetGroups = async (data) => {
    const config = {
      params: {
        study_year: data.study_year || null,
      }
    }
    isGroupLoading.value = true;
    await axiosAPI.get('/assessment/group', config).then((response) => {
      console.log('Список групп успешно получен: ', response.data);
      groups.value = response.data;
    }).finally(() => {
      console.log('Остановка')
      isGroupLoading.value = false;
    });
  };
  return {
    groups, isGroupLoading, fetchGetGroups
  }
}

export function retrieveGroup() {
  const retrievedGroup = ref({});
  const fetchRetrieveGroup = async (group) => {
    await axiosAPI.get(`/assessment/group/${group.id}`).then((response) => {
      console.log('Группа успешно получена', response.data);
      retrievedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    retrievedGroup, fetchRetrieveGroup
  }
}

export function createGroup() {
  const addedGroup = ref({});
  const fetchCreateGroup = async (group) => {
    await axiosAPI.post('/assessment/group', group).then((response) => {
      console.log('Группа успешно добавлена');
      addedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    addedGroup, fetchCreateGroup
  }
}

export function updateGroup() {
  const updatedGroup = ref({});
  const fetchUpdateGroup = async (group) => {
    await axiosAPI.put(`/assessment/group/${group.id}`, group).then((response) => {
      console.log('Группа успешно обновлена', response.data);
      updatedGroup.value = response.data;
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    updatedGroup, fetchUpdateGroup
  }
}

export function deleteGroup() {
  const fetchDeleteGroup = async (group) => {
    await axiosAPI.delete(`/assessment/group/${group}`).then((response) => {
      console.log('Группа успешно удалена');
    }).catch((error) => {
      console.log('Ошибка запроса: ', error);
    });
  };
  return {
    fetchDeleteGroup
  }
}