import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useIboStore = defineStore("ibo", {
  state: () => ({
    learnerProfiles: [],
  }),
  getters: {
    isLearnerProfileLoaded() {
      return (
        this.learnerProfiles.length > 0
      );
    },
  },
  actions: {
    async loadLearnerProfiles(config) {
      const res = await resources.learnerProfile.getLearnerProfiles(config);
      if (res.__state === "success") {
        this.learnerProfiles = res.data
        console.log("IB Learner Profiles успешно получены: ", res.data)
      }
    },

    async loadUnitReflectionPosts(config) {
      return await resources.unitReflectionPost.getUnitReflectionPosts(config);
    },
    async createUnitReflectionPost(post) {
      return await resources.unitReflectionPost.createUnitReflectionPost(post);
    },
    async updateUnitReflectionPost(post) {
      return await resources.unitReflectionPost.updateUnitReflectionPost(post);
    },
    async removeUnitReflectionPost(id) {
      return await resources.unitReflectionPost.removeUnitReflectionPost(id);
    },

    async loadIbProfileDevelops(config) {
      return await resources.ibProfileDevelop.getIbProfileDevelops(config);
    },
    async createIbProfileDevelop(post) {
      return await resources.ibProfileDevelop.createIbProfileDevelop(post);
    },
    async updateIbProfileDevelop(post) {
      return await resources.ibProfileDevelop.updateIbProfileDevelop(post);
    },
    async removeIbProfileDevelop(id) {
      return await resources.ibProfileDevelop.removeIbProfileDevelop(id);
    },
  }
});