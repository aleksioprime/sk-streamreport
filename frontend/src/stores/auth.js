import { defineStore } from "pinia";
import resources from "@/services/resources";
import jwtService from "@/services/jwt/jwt.service";
import JwtService from "@/services/jwt/jwt.service";
import { toast } from 'vue3-toastify';

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
    isAdmin() {
      return !!this.user && this.user.groups.some(i => i.name == 'admin')
    },
    isEmployee() {
      return !!this.user && this.user.groups.some(i => i.name == 'employee')
    },
    isMentor() {
      return !!this.user && this.user.mentor_classes.length
    },
    isTeacher() {
      return this.isEmployee && this.user.teaching_loads.length
    },
    isRole() {
      return this.isEmployee && this.user.group_roles.length
    },
    isTeacherPyp() {
      return this.isEmployee && this.user.teaching_loads.length && this.user.teaching_loads.some(i => i.subject.level == 'noo')
    },
    isStudent() {
      return !!this.user && this.user.groups.some(i => i.name == 'student')
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
      this.user = null;
      jwtService.destroyTokens();
      resources.auth.setAuthHeader("");
    },
    
    // https://vue3-toastify.js-bridge.com/
    showMessageSuccess(message) {
      toast.success(message, {
        autoClose: 2000,
        position: toast.POSITION.BOTTOM_RIGHT,
      });     
    }
  },
});