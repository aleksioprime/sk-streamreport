import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useUnitMypStore = defineStore("unitMyp", {
  state: () => ({
    objectives: [],
  }),
  getters: {
    isObjectivesLoaded() {
      return (
        this.objectives.length > 0
      );
    },
  },
  actions: {
    async loadObjectives(config) {
      const res = await resources.objective.getObjectives(config);
      if (res.__state === "success") {
        this.objectives = res.data
        console.log('Данные успешно загружены: ', res.data)
      }
    },
  }
});