<template>
  <div>
    <div v-if="unit.reflection_posts.length">

      <div v-for="tp in postTypes" :key="tp.id">
        <div><b>{{ tp.name }}</b></div>
        <small>{{ tp.description }}</small>
        <div v-if="unit.reflection_posts.find(i => i.type == tp.value)">
          <div v-for="post in unit.reflection_posts.filter(i => i.type == tp.value)" :key="post.id" class="card my-2">
            <div class="card-body">
              <editable-area v-model="post.post" propName="post" @save="handleSave($event, post.id)" />
              <div class="my-2">{{ post.author.short_name }} <i class="bi bi-dash-square inline-button" @click="showConfirmationModal(post)"></i></div>
            </div>
            <confirmation-modal v-if="post.id == currentUnitReflectionPost.id"
              :nameModal="`confirmationDeleteUnitReflectionPost${post.id}`" @confirm="removeUnitReflectionPost"
              @cancel="cancelUnitReflectionPost">
              Вы действитель хотите удалить эту запись?
            </confirmation-modal>
          </div>
        </div>
        <div v-else class="my-2 card">
          <div class="card-body">
            <div class="d-flex flex-column align-items-center">
              <div>Нет рефлексии в этой категории</div>
            </div>
          </div>
        </div>
      </div>
      <a href="javascript:void(0)" @click.prevent="createFormShow">Добавить рефлексию</a>
    </div>
    <div class="card" v-else>
      <!-- Сообщение о том, что данных нет -->
      <div class="card-body">
        <div class="d-flex flex-column align-items-center">
          <div>Нет информации</div>
          <a href="javascript:void(0)" @click.prevent="createFormShow">Добавить</a>
        </div>
      </div>
    </div>
    <!-- Форма добавления новой записи в таблицу -->
    <div v-if="createMode">
      <div class="card my-2">
        <div class="card-body">
          <simple-dropdown class="my-2" title="Выберите тип поста" v-model="newUnitReflectionPost.type"
            :propItems="postTypes" showName="name" propName="type" />
          <textarea v-model="newUnitReflectionPost.post" class="form-control bottom-border-only my-2" rows="3"
            placeholder="Напишите рефлексию выбранного типа"></textarea>
          <div class="d-flex items-align-center justify-content-end">
            <button class="btn btn-success" @click="createUnitReflectionPost">Добавить</button>
            <button class="btn btn-secondary ms-2" @click="createFormHide">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { Modal } from 'bootstrap';
import { REFLECTION_POST_PYP_TYPES, REFLECTION_POST_TYPES } from "@/common/constants";

import ConfirmationModal from '@/common/components/ConfirmationModal.vue';
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";
import EditableArea from "@/common/components/EditableArea.vue";

import { useIboStore } from "@/stores/ibo";
const iboStore = useIboStore();

import { useUnitPypStore } from "@/stores/unitPyp";
const unitPypStore = useUnitPypStore();

import { useUnitMypStore } from "@/stores/unitMyp";
const unitMypStore = useUnitMypStore();

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const props = defineProps({
  unit: {
    type: Object,
    default: {}
  },
  program: {
    type: String,
    default: '',
  }
});

const postTypes = ref(props.program == 'pyp' ? REFLECTION_POST_PYP_TYPES : REFLECTION_POST_TYPES)

const createMode = ref(false)

// Данные создаваемой записи по умолчанию
const defaultUnitReflectionPost = {
  type: {},
  post: null,
}
const newUnitReflectionPost = ref({ ...defaultUnitReflectionPost })

// ***** Работа с формой по созданию записи *****

// Появление формы для создания записи
const createFormShow = () => {
  createMode.value = true;
}

// Скрытие формы для создания записи
const createFormHide = () => {
  createMode.value = false;
  newUnitReflectionPost.value = { ...defaultUnitReflectionPost }
}

// Подтверждение создания записи и выполнение запроса
const createUnitReflectionPost = () => {
  const createdObject = {
    type: newUnitReflectionPost.value.type.value,
    post: newUnitReflectionPost.value.post,
    unit: props.unit.id,
    author: authStore.user.id,
  };
  console.log(createdObject)
  iboStore.createUnitReflectionPost(createdObject).then((result) => {
    authStore.showMessageSuccess('Пост рефлексии добавлен');
    getUnitReflectionPosts();
  }
  );
  newUnitReflectionPost.value = { ...defaultUnitReflectionPost }
  createMode.value = false;
}

// ***** Работа с модальным окном для удаления записи *****

const currentUnitReflectionPost = ref({})
let confirmationModal = null

// Открыть модальное окно для подтверждения удаления выбранной записи
const showConfirmationModal = (profile) => {
  currentUnitReflectionPost.value = profile
  nextTick(() => {
    confirmationModal = new Modal(`#confirmationDeleteUnitReflectionPost${profile.id}`, { backdrop: 'static' });
    confirmationModal.show();
  });
}

// Отменить удаление выбранной записи и закрыть окно
const cancelUnitReflectionPost = () => {
  confirmationModal.hide();
  currentUnitReflectionPost.value = {};
}

// Удалить выбранную запись и закрыть окно
const removeUnitReflectionPost = () => {
  // console.log('Запрос на удаление участия в мероприятии: ', currentPrimaryTopic.value);
  iboStore.removeUnitReflectionPost(currentUnitReflectionPost.value.id).then(() => {
    authStore.showMessageSuccess('Пост рефлексии удалён');
    getUnitReflectionPosts();
  })
  confirmationModal.hide();
}

// Запрос на получение списка записей для обновления поля
const getUnitReflectionPosts = () => {
  const config = {
    params: {
      unit: props.unit.id
    }
  }
  iboStore.loadUnitReflectionPosts(config).then((result) => {
    if (props.program == 'pyp') {
      unitPypStore.pypUnit.reflection_posts = [...result.data]
    } else if (props.program == 'myp') {
      return
    } else if (props.program == 'dp') {
      return
    }
  })
}

// Функция редактирования конкретного поля
const handleSave = async (editData, id) => {
  const updatingData = {
    id: id,
    [editData.propName]: editData.value,
  }
  iboStore.updateUnitReflectionPost(updatingData).then((result) => {
    authStore.showMessageSuccess('Сохранено');
    if (props.program == 'pyp') {
      unitPypStore.pypUnit.reflection_posts = unitPypStore.pypUnit.reflection_posts.map(item => item.id === result.data.id ? { ...result.data } : item);
    } else if (props.program == 'myp') {
      return
    } else if (props.program == 'dp') {
      return
    }
  })
};
</script>