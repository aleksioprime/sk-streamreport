<template>
  <div class="modal fade" :id="nameModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel"
    data-bs-backdrop="static" aria-hidden="true">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalLabel">{{ titleModal }}</h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Закрыть" @click="cancelModal"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelModal">Отмена</button>
          <button type="button" class="btn btn-success" @click="confirm">{{ titleConfirm }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>

const props = defineProps({
  titleConfirm: {
    type: String,
    default: ''
  },
  titleModal: {
    type: String,
    default: '',
  },
  nameModal: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['confirm', 'cancel']);

const confirm = () => {
  emit('confirm');
}

const cancelModal = () => {
  emit('cancel');
}
</script>