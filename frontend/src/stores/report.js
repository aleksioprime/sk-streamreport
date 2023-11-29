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
            ...item, 
            full_name: capitalizeFirstLetter(item.name) 
          };
        });
      }
    },
    async loadStudentExtraReports(config) {
      const res = await resources.studentExtraReport.getStudentExtraReports(config);
      if (res.__state === "success") {
        this.studentExtraReports = res.data.map(item => {
          return {
            ...item,
            report: item.reports[0]
          };
        });
      }
    },
    async createReportExtra(report) {
      return await resources.reportExtra.createReportExtra(report);
    },
    async updateReportExtra(report) {
      return await resources.reportExtra.updateReportExtra(report);
    },
    async removeReportExtra(report) {
      return await resources.reportExtra.removeReportExtra(report);
    },
  }
});