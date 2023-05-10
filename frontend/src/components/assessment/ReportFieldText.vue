<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Отчёт по студенту</div>
      <button v-if="!editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div v-html="student.teacher_report.text"></div> 
        </div>
        <div v-else>
          <div class="field-description">Введите описание</div>
          <div v-if="!isGPTTextLoading">
            <editor api-key="j30bef5hr2ipfdbu7b9lww7t4oez2v6f27c94otp9to2j9mk"
              :init="{
                plugins: 'lists link wordcount autoresize',
                menubar: false,
                toolbar: 'undo redo | bold italic | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist '
              }"
              model-events="change keydown blur focus paste" output-format="html" v-model="editData.text"/>
          </div>
          <div v-else class="loader">
            <div class="lds-spinner">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
          <div class="field-buttons">
            <button class="field-btn-generate" @click="generateField">Сгенерировать</button>
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
import Editor from '@tinymce/tinymce-vue';
import { getChatGPTReport } from "@/hooks/assess/useGenerateReport";

export default {
  name: 'ReportFieldText',
  components: {
    'editor': Editor
  },
  props: {
    student: { 
      type: Object, 
      default: {
        teacher_report: {},
        user: {},
      }
    },
    criteria: {
      type: Object,
      default: {}
    }
  },
  setup(props) {
    const { generatedGPTText, isGPTTextLoading, fetchChatGPTReport } = getChatGPTReport();
    return {
      generatedGPTText, isGPTTextLoading, fetchChatGPTReport
    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
    }
  },
  methods: {
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData)
    },
    cancelField() {
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      this.editData.text = this.student.teacher_report.text;
    },
    generateField() {
      const data = {
        mark: {
          criterion_a: this.student.periodassess.criterion_a,
          criterion_b: this.student.periodassess.criterion_b,
          criterion_c: this.student.periodassess.criterion_c,
          criterion_d: this.student.periodassess.criterion_d,
        },
        criteria: this.criteria,
        first_name: this.student.user.first_name,
        subject: this.student.teacher_report.subject.name_rus
      }
      this.fetchChatGPTReport(data).finally(() => {
        this.editData.text = this.generatedGPTText;
      });
    }
  },
}
</script>
<style>
@import '@/assets/css/spinner.css';
.loader {
  display: flex;
  height: 200px;
  align-items: center;
  justify-content: center;
}
.field-btn-generate {
  border: none;
  border-radius: 5px;
  background-color: #33cc40;
  color: #fff;
  padding: 3px 8px;
  margin-left: auto;
  font-size: 0.8em;
}
</style>