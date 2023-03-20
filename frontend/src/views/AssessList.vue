<template>
  <div>
    <base-header>
      <template v-slot:header>Итоговые работы</template>
    </base-header>
    <button type="button" class="btn btn-primary ms-auto mb-2 w-100" @click="showAssessModalAdd">
      Cоздать итоговую работку
    </button>
    <!-- Модальное окно добавления/редактирования/удаления итоговой работы -->
    <modal-assess :modalTitle="modalTitle" @cancel="hideAssessModal">
      <template v-slot:body>
        <!-- Форма добавления/редактирования итоговой работы -->
        <assess-form v-if="flagAssess.add || flagAssess.edit" v-model="currentAssess" />
        <!-- Текст удаления итоговой работы -->
        <div v-if="flagAssess.delete">Вы действительно хотите удалить эту итоговую работу?</div>
      </template>
    </modal-assess>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import AssessForm from "@/components/AssessForm.vue";

export default {
  name: 'Assessment',
  components: {
    AssessForm,
  },
  data() {
    return {
      modalAssess: {},
      modalTitle: '',
      flagAssess: {
        add: false,
        edit: false,
        delete: false,
      },
      currentAssess: {},
    }
  },
  methods: {
    hideAssessModal() {
      this.modalAssess.hide();
    },
    showAssessModalAdd() {
      this.modalTitle = 'Создание пользователя';
      this.modalAssess.show();
      this.flagAssess.add = true;
    },
    showAssessModalEdit() {

    },
    showAssessModalDelete() {

    },
  },
  mounted() {
    // Инициализация объекта модального окна
    this.modalAssess = new Modal('#modalAssess', { backdrop: 'static' });
  },
}
</script>

<style></style>