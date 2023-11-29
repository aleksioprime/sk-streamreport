import { defineStore } from "pinia";

import resources from "@/services/resources";
import {
  capitalizeFirstLetter,
} from "@/common/helpers/processingText";

export const useReportStore = defineStore("report", {
  state: () => ({
    reportPeriods: [],
    studentExtraReports: [],
  }),
  getters: {
    isReportPeriodsLoaded() {
      return (
        this.reportPeriods.length > 0
      );
    },
    isStudentExtraReportsLoaded() {
      return (
        this.studentExtraReports.length > 0
      );
    },
  },
  actions: {
    async loadReportPeriods() {
      const res = await resources.reportPeriod.getReportPeriods();
      if (res.__state === "success") {
        this.reportPeriods = res.data.map(item => {
          return {
            ...item, // Копирование всех существующих свойств
            full_name: capitalizeFirstLetter(item.name) // Добавление нового свойства name
          };
        });
      }
    },
    async loadStudentExtraReports(config) {
      const res = await resources.studentExtraReport.getStudentExtraReports(config);
      if (res.__state === "success") {
        this.studentExtraReports = res.data
      }
    },
  }
});