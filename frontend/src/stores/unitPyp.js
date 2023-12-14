import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useUnitPypStore = defineStore("unitPyp", {
  state: () => ({
    pypUnits: [],
    pypUnit: {},
    transdisciplinaryThemes: [],
    pypAtlSkills: [],
    pypAtlClusters: [],
    pypKeyConcepts: [],
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
    async loadPypAtlSkills(config) {
      const res = await resources.pypAtlSkill.getPypAtlSkills(config);
      if (res.__state === "success") {
        this.pypAtlSkills = res.data
        console.log('Навыки ATL для PYP успешно загружены: ', res.data)
      }
    },
    async loadPypAtlClusters(config) {
      const res = await resources.pypAtlCluster.getPypAtlClusters(config);
      if (res.__state === "success") {
        this.pypAtlClusters = res.data
        console.log('Кластеры ATL для PYP успешно загружены: ', res.data)
      }
    },
    async loadPypKeyConcepts(config) {
      const res = await resources.pypKeyConcept.getPypKeyConcepts(config);
      if (res.__state === "success") {
        this.pypKeyConcepts = res.data
        console.log('Ключевые концепты для PYP успешно загружены: ', res.data)
      }
    },
    
    async loadPypAtlDevelops(config) {
      return await resources.pypAtlDevelop.getPypAtlDevelops(config);
    },
    async createPypAtlDevelop(atl) {
      return await resources.pypAtlDevelop.createPypAtlDevelop(atl);
    },
    async updatePypAtlDevelop(atl) {
      return await resources.pypAtlDevelop.updatePypAtlDevelop(atl);
    },
    async removePypAtlDevelop(id) {
      return await resources.pypAtlDevelop.removePypAtlDevelop(id);
    },

    async loadPypLinesOfInquiries(config) {
      return await resources.pypLinesOfInquiry.getPypLinesOfInquiries(config);
    },
    async createPypLinesOfInquiry(atl) {
      return await resources.pypLinesOfInquiry.createPypLinesOfInquiry(atl);
    },
    async updatePypLinesOfInquiry(atl) {
      return await resources.pypLinesOfInquiry.updatePypLinesOfInquiry(atl);
    },
    async removePypLinesOfInquiry(id) {
      return await resources.pypLinesOfInquiry.removePypLinesOfInquiry(id);
    },

    async loadPypRelatedConcepts(config) {
      return await resources.pypRelatedConcept.getPypRelatedConcepts(config);
    },
    async createPypRelatedConcept(atl) {
      return await resources.pypRelatedConcept.createPypRelatedConcept(atl);
    },
    async updatePypRelatedConcept(atl) {
      return await resources.pypRelatedConcept.updatePypRelatedConcept(atl);
    },
    async removePypRelatedConcept(id) {
      return await resources.pypRelatedConcept.removePypRelatedConcept(id);
    },
  }
});