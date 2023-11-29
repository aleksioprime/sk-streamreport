<template>
  <div class="modal fade" id="confirmationModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel" data-bs-backdrop="static" 
    aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalLabel">Подтвердите действие</h5>
          <button type="button" class="btn-close" data-dismiss="modal" aria-label="Закрыть" @click="cancelModal"></button>
        </div>
        <div class="modal-body">
          <slot />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelModal">Отмена</button>
          <button type="button" class="btn btn-danger" @click="confirm">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

const emit = defineEmits(['confirm', 'cancel']);

const confirm = () => {
  emit('confirm');
}

const cancelModal = () => {
  emit('cancel');
}
</script>