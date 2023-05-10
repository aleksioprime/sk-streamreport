<template>
  <div class="sumworks-item">
    <div class="title">
      <div class="text">{{ sumwork.title }}</div>
      <div class="tools">
        <div class="btn edit" @click="$emit('editWork', sumwork)"></div>
        <div class="btn delete" @click="$emit('deleteWork', sumwork)"></div>
      </div>
    </div>
    <div class="teacher">Учитель:&nbsp;{{ sumwork.teacher.user.last_name }} {{ sumwork.teacher.user.first_name }} {{ sumwork.teacher.user.middle_name }}</div>
    <div class="unit">
      <div>Юнит:&nbsp;
        <a :href="`/unit/${sumwork.unit.id}`">{{ sumwork.unit.title }}</a> 
        <span v-if="sumwork.unit.interdisciplinary" class="badge rounded-pill text-bg-primary me-1">МДП<br></span>
      </div>
      <div>Предмет: {{ sumwork.unit.subject.name_rus }}</div>
    </div>
    
    <div class="assessment">
      <div class="criteria">
        <div class="criteria-title">Критерии оценки:</div>
        <div class="criteria-item" :class="classCriteria(cr.letter)" v-for="cr in sumwork.criteria" :key="cr.id">{{ cr.letter }}</div>
      </div>
      <div v-if="sumwork.groups.length">
        <div class="group-title">Журналы оценок:</div>
        <div class="groups">
          <div class="group" v-for="gr in sumwork.groups" :key="gr.id" @click="$router.push(`/assessment/sumwork/${gr.id}`)">
            <div class="group-name">{{ gr.group.class_year }}{{ gr.group.letter }} класс</div>
            <div class="group-date">{{ new Date(gr.date).toLocaleDateString() }}</div>
          </div>
        </div>
      </div>
      <div v-else>Не выбраны классы</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    sumwork: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {

    }
  },
  methods: {
    classCriteria(letter) {
      if (letter.toLowerCase() == 'a') {
        return 'criteria-a'
      } else if (letter.toLowerCase() == 'b') {
        return 'criteria-b'
      } else if (letter.toLowerCase() == 'c') {
        return 'criteria-c'
      } else {
        return 'criteria-d'
      }
    },
  }
}
</script>

<style>
.sumworks-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #c4c4c4;
  border-radius: 10px;
}
.sumworks-item .title {
  display: flex;
}
.sumworks-item .title .text {
  color: #1e7979;
  font-weight: 700;
}
.sumworks-item .tools {
  display: flex;
  margin-left: auto;
}
.sumworks-item .tools .btn {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
}
.btn.edit {
  background: url('@/assets/img/item-edit.png') no-repeat 50% / 90%;
  margin-right: 5px;
}
.btn.delete {
  background: url('@/assets/img/item-delete.png') no-repeat 50% / 90%;
}
.sumworks-item .unit {
  margin-bottom: 10px;
}

.sumworks-item .assessment {
  display: flex;
  align-items: flex-start;
}
.sumworks-item .criteria {
  display: flex;
  flex-wrap: wrap;
  width: 170px;
}
.sumworks-item .criteria-item {
  margin-right: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  font-weight: 700;
}
.sumworks-item .criteria-title {
  margin-right: 5px;
  margin-bottom: 10px;
  flex-grow: 1;
  flex-basis: 100%;
}
.sumworks-item .assessment .groups {
  display: flex;
  flex-wrap: wrap;
  padding-bottom: 5px;
}
.sumworks-item .assessment .group {
  box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
  padding: 5px 15px;
  text-align: center;
  border-radius: 10px;
  cursor: pointer;
}
.sumworks-item .assessment .group:not(:last-of-type) {
  margin-right: 10px
}
.sumworks-item .assessment .group:hover {
  background: #c4c4c4;
  color: #ffffff;
}
.sumworks-item .group-title {
  margin-bottom: 10px;
  flex-grow: 1;
  flex-basis: 100%;
}
.sumworks-item .group-name {
  font-weight: 700;
}
.sumworks-empty 
{
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 30vh;
}

@media screen and (max-width: 540px) {
  .sumworks-item .assessment .groups {
    border: none;
    margin-top: 5px;
    padding: 0;
  }
  .sumworks-item .assessment {
    flex-direction: column;
  }
}

.criteria-a {
  color: #54C3DA;
  border: 1px solid #54C3DA;
}

.criteria-b {
  color: #a59a50;
  border: 1px solid #a59a50;
}

.criteria-c {
  color: #7AC11A;
  border: 1px solid #7AC11A;
}

.criteria-d {
  color: #CA4348;
  border: 1px solid #CA4348;
}
</style>