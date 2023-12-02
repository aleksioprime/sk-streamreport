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
  }
});