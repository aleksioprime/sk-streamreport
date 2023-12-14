import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useUnitMypStore = defineStore("unitMyp", {
  state: () => ({
    objectives: [],
    strands: [],
  }),
  getters: {
    isObjectivesLoaded() {
      return (
        this.objectives.length > 0
      );
    },
    isStrandsLoaded() {
      return (
        this.strands.length > 0
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
    async loadStrands(config) {
      const res = await resources.strand.getStrands(config);
      if (res.__state === "success") {
        this.strands = res.data
        console.log('Данные успешно загружены: ', res.data)
      }
    },
  }
});