import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useUnitPypStore = defineStore("unitPyp", {
  state: () => ({
    pypUnits: [],
    pypUnit: {},
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
  }
});