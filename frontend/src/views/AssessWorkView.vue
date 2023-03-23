<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за итоговую работу</template>
    </base-header>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  name: 'AssessWorkView',
  components: {
    
  },
  setup(props) {
    return {
      
    }
  },
  data() {
    return {
      modalStudents: {}
    }
  },
  methods: {
    
  },
  mounted() {
    this.modalStudents = new Modal(`#modalStudents`, { backdrop: 'static' });
  },
  computed: {
  }
}
</script>

<style scoped>

</style>