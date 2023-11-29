import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useCurriculumStore = defineStore("curriculum", {
  state: () => ({
    subjects: [],
    curriculums: [],
    groups: [],
  }),
  getters: {
    isSubjectsLoaded() {
      return (
        this.subjects.length > 0
      );
    },
  },
  actions: {
    async loadSubjects() {
      const res = await resources.subject.getSubjects();
      if (res.__state === "success") {
        this.subjects = res.data
      }
    },
    async loadCurriculums() {
      const res = await resources.subject.getCurriculums();
      if (res.__state === "success") {
        this.curriculums = res.data
      }
    },
    async loadGroups() {
      const res = await resources.subject.getGroups();
      if (res.__state === "success") {
        this.groups = res.data
      }
    }
  }
});