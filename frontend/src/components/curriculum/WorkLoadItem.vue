<template>
  <div class="subject-item area">
    <div><h3>{{ subject.name_rus }}<small v-if="subject.group_ib">&nbsp;({{ subject.group_ib.program.toUpperCase() }}: {{ subject.group_ib.name_eng }})</small></h3></div>
    <div>{{ subject.type_name }}</div>
    <div v-if="subject.group_fgos">{{ subject.group_fgos.type_name }}: {{ subject.group_fgos.name_rus }}</div>
    <div class="collapse-title collapsed" data-bs-toggle="collapse" :href="`#collapse-${subject.id}`" role="button" aria-expanded="false" :aria-controls="`#collapse-${subject.id}`">Нагрузка предмета по кафедре</div>
    <div class="workload-wrapper collapse" :id="`collapse-${subject.id}`">    
      <div class="workload-container" v-if="subject.workload.length">
        <!-- <div v-for="(groupsByYear, year) in groupedArrayData(subject.workload, ['groups', 'class_year'])" :key="year" class="workload-grouped-item">
          {{ year }} классы -->
          <div v-for="wl in subject.workload" :key="wl.id" class="workload-item">
            <div>
              <div><span v-for="gr, index in wl.groups" :key="gr.id">{{ gr.group_name }}<span v-if="++index !== wl.groups.length">,&nbsp;</span></span>: {{ getWordHour(wl.hours) }}</div>
              <div class="subject-teacher">{{ wl.teacher.short_name }}</div>
            </div>
            <button class="icon icon-del" @click="$emit('deleteItem', wl)"></button>
          </div>
        <!-- </div> -->
      </div>
      <div v-else class="workload-none">Часов нагрузки данного предмета пока не добавлено</div>
      <slot name="form"></slot>
    </div>
    
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'WorkLoadItem',
  components: {
  },
  props: {
    subject: {
      type: Object,
      default: {}
    },
  },
  setup(props) {
    const { groupedArrayData } = getGroupedArray();
    return {
      groupedArrayData
    }
  },
  data() {
    return {
      editableWorkLoad: null,
    }
  },
  methods: {
    getWordHour(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} часов`;
      if (number > 1 && number < 5) return `${count} часа`;
      if (number == 1) return `${count} час`;
      return `${count} часов`;
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>

<style scoped>
.subject-item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  margin-top: 10px;
}
.workload-wrapper {
  /* overflow-x: scroll; */
  padding: 10px;
}
.workload-none {
  padding: 10px 0;
}
.workload-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  /* min-width: 700px; */
}
.workload-grouped-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 200px;
}
.workload-item {
  display: flex;
  flex-direction: column;
  column-gap: 10px;
  padding: 5px;
  border: 1px solid #674A9E;
  border-radius: 5px;
  position: relative;
  min-width: 130px;
}
.subject-teacher {
  font-size: 0.8em;
}
.icon {
  position: absolute;
  right: 5px;
  top: 5px;
  width: 20px;
  height: 20px;
}
</style>