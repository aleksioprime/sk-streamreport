import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useUnitPypStore = defineStore("unitPyp", {
  state: () => ({
    pypUnits: [],
    pypUnit: {},
    transdisciplinaryThemes: [],
  }),
  getters: {

  },
  actions: {
    async loadPypUnitPlanners(config) {
      const res = await resources.pypUnitPlanner.getPypUnitPlanners(config);
      if (res.__state === "success") {
        this.pypUnits = res.data
        console.log('Данные юнитов PYP успешно загружены: ', res.data)
      }
    },
    async loadPypUnitPlannerDetail(config) {
      const res = await resources.pypUnitPlanner.retrievePypUnitPlanner(config);
      if (res.__state === "success") {
        this.pypUnit = res.data
        console.log('Данные юнита PYP успешно загружены: ', res.data)
      }
    },
    async createPypUnitPlanner(unit) {
      return await resources.pypUnitPlanner.createPypUnitPlanner(unit);
    },
    async updatePypUnitPlanner(unit) {
      return await resources.pypUnitPlanner.updatePypUnitPlanner(unit);
    },
    async removePypUnitPlanner(unit) {
      return await resources.pypUnitPlanner.removePypUnitPlanner(unit);
    },
    async loadTransdisciplinaryThemes(config) {
      const res = await resources.transdisciplinaryTheme.getTransdisciplinaryThemes(config);
      if (res.__state === "success") {
        this.transdisciplinaryThemes = res.data
        console.log('Трансдисциплинарные темы для PYP успешно загружены: ', res.data)
      }
    },
  }
});