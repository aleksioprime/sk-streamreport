import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useCurriculumStore = defineStore("curriculum", {
  state: () => ({
    subjects: [],
    curriculums: [],
  }),
  getters: {
    isSubjectsLoaded() {
      return (
        this.subjects.length > 0
      );
    },
  },
  actions: {
    async loadSubjects(config) {
      const res = await resources.subject.getSubjects(config);
      if (res.__state === "success") {
        
        this.subjects = res.data.map(item => {
          let name_ib = item.group_ib ? `${item.name} (${item.group_ib.name})` : `${item.name}`
          return {
            ...item, // Копирование всех существующих свойств
            name_ib: name_ib,
            name_level: `${item.name} (${item.level_name})`,
          };
        });
        console.log('Предметы успешно загружены: ', this.subjects)
      }
    },
    async loadCurriculums(config) {
      const res = await resources.curriculum.getCurriculums(config);
      if (res.__state === "success") {
        this.curriculums = res.data
      }
    },

    async loadTeachingLoads(config) {
      return await resources.teachingLoad.getTeachingLoads(config);
    },
    async createTeachingLoad(load) {
      return await resources.teachingLoad.createTeachingLoad(load);
    },
    async updateTeachingLoad(load) {
      return await resources.teachingLoad.updateTeachingLoad(load);
    },
    async removeTeachingLoad(id) {
      return await resources.teachingLoad.removeTeachingLoad(id);
    },
  }
});