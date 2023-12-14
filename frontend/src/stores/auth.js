import { defineStore } from "pinia";
import resources from "@/services/resources";
import jwtService from "@/services/jwt/jwt.service";
import JwtService from "@/services/jwt/jwt.service";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    alertSuccess: false,
    animationClass: null,
    alertSuccessMessage: null,
  }),
  getters: {
    isAuthenticated() {
      return !!this.user;
    },
  },
  actions: {
    setUser(user) {
      this.user = user;
    },

    setPhoto(photo) {
      this.user.photo = photo;
    },

    async login(credentials) {
      const res = await resources.auth.login(credentials);
      if (res.__state === "success") {
        jwtService.saveAccessToken(res.data.access);
        jwtService.saveRefreshToken(res.data.refresh);
        return "success";
      } else {
        return res.data.message;
      }
    },

    async whoami() {
      resources.auth.setAuthHeader(JwtService.getAccessToken());
      const res1 = await resources.auth.whoami();
      if (res1.__state !== "success") {
        await this.logout();
        return;
      } else {
        this.setUser(res1.data);
        console.log('Получены данные авторизированного пользователя: ', res1.data)
      }
    },

    async logout() {
      // await resources.auth.logout();
      jwtService.destroyTokens();
      resources.auth.setAuthHeader("");
      this.user = null;
    },

    showMessageSuccess(message) {
      this.animationClass = 'animate__fadeInDown';
      this.alertSuccessMessage = message
      this.alertSuccess = true;
      // Скрыть сообщение через 3 секунды
      setTimeout(() => {
        this.animationClass = 'animate__fadeOutUp';
        setTimeout(() => {
          this.alertSuccess = false;
          this.alertSuccessMessage = null
        }, 1000)
        
      }, 3000);
      
    }
  },
});