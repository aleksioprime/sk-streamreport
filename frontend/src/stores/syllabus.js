import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useSyllabusStore = defineStore("syllabus", {
  state: () => ({
    courses: [],
  }),
  getters: {
    isCoursesLoaded() {
      return (
        this.courses.length > 0
      );
    },
  },
  actions: {
    async loadCourses(config) {
      const res = await resources.course.getCourses(config);
      if (res.__state === "success") {
        this.courses = res.data
        console.log(res.data)
      }
    },
  }
});