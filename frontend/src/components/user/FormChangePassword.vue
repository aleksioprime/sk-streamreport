<template>
  <div>
    <form>
      <div class="my-2">
        {{ editedUser.full_name }}
      </div>
      <div class="row">
        <div class="col-md mt-2">
          <label for="pass" class="form-label">Пароль:</label>
          <input id="pass" class="form-control" type="password" autocomplete="new-password" v-model="editedUser.password" 
          @input="updateFieldUnit('password', $event.target.value)" required>
          <small ref="password_alert" class="alert-text"></small>
        </div>
        <div class="col-md mt-2">
          <label for="pass-repeat" class="form-label">
            Повторите пароль:</label>
          <input id="pass-repeat" class="form-control" type="password" v-model="editedUser.password_repeat" 
            @input="updateFieldUnit('password_repeat', $event.target.value)" autocomplete="new-password" required>
          <small ref="password_repeat_alert" class="alert-text"></small>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { toRefs } from 'vue'

export default {
  props: {
    editedUser: { type: Object, default: {} },
    validFormChangePassword: { type: Boolean },
  },
  setup() {
    return { };
  },
  data() {
    return {
      textAlert: {
        password: 'Введите пароль',
        password_repeat: 'Повторите правильно пароль',
      },
      errorField: {},
    }
  },
  methods: {
    // Проверка каждого поля формы на правильность введённых данных
    checkFieldsValidate() {
      this.editedUser.password ? this.errorField.password = false : this.errorField.password = true;
      this.editedUser.password && this.editedUser.password_repeat == this.editedUser.password ? this.errorField.password_repeat = false : this.errorField.password_repeat = true;
      const validate = Object.values(this.errorField).every(item => item == false)
      this.$emit('update:validFormChangePassword', validate);
      this.validateForm();
    },
    // Валидация формы - проверка ошибок полей формы и вывод их в виде текста на форму
    validateForm() {
      for (let key in this.errorField) {
        if (this.$refs[`${key}_alert`]) {
          if (this.errorField[key]) {
            this.$refs[`${key}_alert`].innerText = this.textAlert[key];
          } else {
            this.$refs[`${key}_alert`].innerText = "";
          }
        }
      }
    },
    // Обновление данных создаваемого пользователя (переменной editedUser из родительского компонента)
    updateFieldUnit(key, value) {
      this.$emit('update:editedUser', {...this.editedUser, [key]: value });
      this.checkFieldsValidate();
    },
  },
}
</script>

<style scoped>
 .alert-text {
    color: red;
  }
  .alert-field {
    border-color: red;
  }
  .field-admin {
    margin-top: 15px;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 5px;
  }
</style>