<template>
  <div>
    <base-header>
      <template v-slot:link><a href="/assessment">Вернуться к списку итоговых работ</a></template>
      <template v-slot:header>Журнал оценок за период</template>
    </base-header>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  name: 'AssessPeriodView',
  components: {
    
  },
  setup(props) {
    return {
      
    }
  },
  data() {
    return {
      modalAssessment: {}
    }
  },
  methods: {
    
  },
  mounted() {
    this.modalAssessment = new Modal(`#modalAssessment`, { backdrop: 'static' });
  },
  computed: {
  }
}
</script>

<style scoped>

</style>