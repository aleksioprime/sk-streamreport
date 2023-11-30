import { defineStore } from "pinia";

import resources from "@/services/resources";
import {
  capitalizeFirstLetter,
} from "@/common/helpers/processingText";

export const useReportStore = defineStore("report", {
  state: () => ({
    reportPeriods: [],
    studentExtraReports: [],
    reportTeachers: [],
    reportTeachersPrimary: [],
    reportTeachersSecondary: [],
    reportTeachersHigh: []
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
    isReportTeachersPrimaryLoaded() {
      return (
        this.reportTeachersPrimary.length > 0
      );
    },
    isReportTeachersSecondaryLoaded() {
      return (
        this.reportTeachersSecondary.length > 0
      );
    },
    isReportTeachersHighLoaded() {
      return (
        this.reportTeachersHigh.length > 0
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
    async loadReportTeachersPrimary(config) {
      const res = await resources.reportTeacherPrimary.getReportTeachersPrimary(config);
      if (res.__state === "success") {
        this.reportTeachersPrimary = res.data
        this.reportTeachers = res.data
      }
    },
    async createReportTeacherPrimary(report) {
      return await resources.reportTeacherPrimary.createReportTeacherPrimary(report);
    },
    async updateReportTeacherPrimary(report) {
      return await resources.reportTeacherPrimary.updateReportTeacherPrimary(report);
    },
    async removeReportTeacherPrimary(report) {
      return await resources.reportTeacherPrimary.removeReportTeacherPrimary(report);
    },
    async loadReportTeachersSecondary(config) {
      const res = await resources.reportTeacherSecondary.getReportTeachersSecondary(config);
      if (res.__state === "success") {
        this.reportTeachersSecondary = res.data
        this.reportTeachers = res.data
      }
    },
    async createReportTeacherSecondary(report) {
      return await resources.reportTeacherSecondary.createReportTeacherSecondary(report);
    },
    async updateReportTeacherSecondary(report) {
      return await resources.reportTeacherSecondary.updateReportTeacherSecondary(report);
    },
    async removeReportTeacherSecondary(report) {
      return await resources.reportTeacherSecondary.removeReportTeacherSecondary(report);
    },
    async loadReportTeachersHigh(config) {
      const res = await resources.reportTeacherHigh.getReportTeachersHigh(config);
      if (res.__state === "success") {
        this.reportTeachersHigh = res.data
        this.reportTeachers = res.data
      }
    },
    async createReportTeacherHigh(report) {
      return await resources.reportTeacherHigh.createReportTeacherHigh(report);
    },
    async updateReportTeacherHigh(report) {
      return await resources.reportTeacherHigh.updateReportTeacherHigh(report);
    },
    async removeReportTeacherHigh(report) {
      return await resources.reportTeacherHigh.removeReportTeacherHigh(report);
    },
    // CRUD для академических результатов студентов начальной школы
    async createReportPrimaryTopic(report) {
      return await resources.reportPrimaryTopic.createReportPrimaryTopic(report);
    },
    async updateReportPrimaryTopic(report) {
      return await resources.reportPrimaryTopic.updateReportPrimaryTopic(report);
    },
    async removeReportPrimaryTopic(id) {
      return await resources.reportPrimaryTopic.removeReportPrimaryTopic(id);
    },
  }
});