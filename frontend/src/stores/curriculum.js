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
        this.subjects = res.data
      }
    },
    async loadCurriculums(config) {
      const res = await resources.curriculum.getCurriculums(config);
      if (res.__state === "success") {
        this.curriculums = res.data
      }
    },
  }
});