<template>
  <div class="login">
    <div class="form-signin w-100 m-auto">
      <form @submit.prevent="login">
        <img class="mb-3" src="@/assets/img/sk_report_logo_notext.svg" alt="" width="100">
        <h1 class="h3 mb-3 fw-normal">Войти в систему</h1>
        <div class="form-floating">
          <input type="email" name="email" class="form-control" id="floatingInput" placeholder="example@mail.ru"
            v-model="email" />
          <label for="floatingInput">Пользователь</label>
        </div>
        <div class="alert alert-danger" v-if="validations.email.error">{{ validations.email.error }}</div>
        <div class="form-floating">
          <input type="password" class="form-control" id="floatingPassword" placeholder="********" v-model="password" />
          <label for="floatingPassword">Пароль</label>
        </div>
        <div class="alert alert-danger" v-if="validations.password.error">{{ validations.password.error }}</div>
        <!-- <div class="checkbox mb-3">
          <label for="rememberMe">
            <input id="rememberMe" type="checkbox" value="remember-me"> Запомнить меня
          </label>
        </div> -->
        <button class="w-100 btn btn-lg btn-primary" type="submit">Войти</button> 
        <div v-if="isLoadedRequest" class="loader-line"></div>
        <div class="alert alert-danger mt-2" v-if="errorMessage">
          {{ errorMessageText }}
        </div>
        <p class="mt-5 mb-3 text-muted">&copy; ОЧУ МГ Сколково 2023</p>
      </form>
    </div>
  </div>
</template>
  
<script setup>
import { ref, watch, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { clearValidationErrors, validateFields } from "@/common/validator";

const authStore = useAuthStore();
const router = useRouter();

const resetValidations = () => {
  return {
    email: {
      error: "",
      rules: ["required", "email"],
    },
    password: {
      error: "",
      rules: ["required"],
    },
  };
};

const email = ref("");
const password = ref("");
const validations = ref(resetValidations());
const errorMessage = ref(null);

const isLoadedRequest = ref(false)

const errorMessageText = computed(() => {
      const errorMessages = {
        'Request failed with status code 400': 'Неверные учетные данные. Попробуйте снова',
        'Request failed with status code 500': 'Сервер в данный момент недоступен. Попробуйте позже',
        // Добавьте здесь другие коды ошибок и сообщения
      };

      // Возвращаем сообщение об ошибке или общее сообщение для неизвестных ошибок
      return errorMessages[errorMessage.value] || 'Произошла ошибка. Попробуйте снова позже.';
    })

const watchField = (field) => () => {
  if (errorMessage.value) {
    errorMessage.value = null;
  }

  if (validations.value[field]?.error) {
    clearValidationErrors(validations.value);
  }
};

watch(email, watchField("email"));
watch(password, watchField("password"));

const login = async () => {
  isLoadedRequest.value = true;
  const isValid = validateFields(
    { email: email.value, password: password.value },
    validations.value
  );

  if (!isValid) {
    return;
  }

  const resMsg = await authStore.login({
    email: email.value.toLocaleLowerCase(),
    password: password.value,
  });
  
  if (resMsg === "success") {
    await authStore.whoami();
    await router.push({ name: "home" });
    
  } else {
    errorMessage.value = resMsg;
  }
  isLoadedRequest.value = false;
};
</script>
  
<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
  text-align: center;
}

.form-signin {
  max-width: 330px;
  padding: 1rem;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>