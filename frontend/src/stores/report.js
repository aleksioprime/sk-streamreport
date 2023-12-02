import { defineStore } from "pinia";

import resources from "@/services/resources";
import {
  capitalizeFirstLetter,
} from "@/common/helpers/processingText";

export const useReportStore = defineStore("report", {
  state: () => ({
    levels: [
      {value: 'a', name: 'A'},
      {value: 'b', name: 'B'},
      {value: 'c', name: 'C'},
      {value: null, name: 'Нет'}
    ],
    reportPeriods: [],
    reportCriteria: [],
    studentExtraReports: [],
    studentMentorReports: [],
    reportTeachers: [],
    // reportTeachersPrimary: [],
    // reportTeachersSecondary: [],
    // reportTeachersHigh: []
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
    async loadReportCriteria(config) {
      const res = await resources.reportCriterion.getReportCriteria(config);
      if (res.__state === "success") {
        this.reportCriteria = res.data
        console.log(res)
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
        // this.reportTeachersPrimary = res.data
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
        // this.reportTeachersSecondary = res.data
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
        // this.reportTeachersHigh = res.data
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
    async loadReportPrimaryTopics(config) {
      return await resources.reportPrimaryTopic.getReportPrimaryTopics(config);
    },
    async createReportPrimaryTopic(report) {
      return await resources.reportPrimaryTopic.createReportPrimaryTopic(report);
    },
    async updateReportPrimaryTopic(report) {
      return await resources.reportPrimaryTopic.updateReportPrimaryTopic(report);
    },
    async removeReportPrimaryTopic(id) {
      return await resources.reportPrimaryTopic.removeReportPrimaryTopic(id);
    },
    // CRUD для достижений студентов по критериям учителя
    async loadReportTeacherAchievements(config) {
      return await resources.reportTeacherAchievement.getReportTeacherAchievements(config);
    },
    async createReportTeacherAchievement(report) {
      return await resources.reportTeacherAchievement.createReportTeacherAchievement(report);
    },
    async updateReportTeacherAchievement(report) {
      return await resources.reportTeacherAchievement.updateReportTeacherAchievement(report);
    },
    async removeReportTeacherAchievement(id) {
      return await resources.reportTeacherAchievement.removeReportTeacherAchievement(id);
    },
    
    async loadStudentMentorReports(config) {
      const res = await resources.studentMentorReport.getStudentMentorReports(config);
      if (res.__state === "success") {
        this.studentMentorReports = res.data.map(item => {
          return {
            ...item,
            report: item.reports[0]
          };
        });
      }
    },
    async createReportMentor(report) {
      return await resources.reportMentor.createReportMentor(report);
    },
    async updateReportMentor(report) {
      return await resources.reportMentor.updateReportMentor(report);
    },
    async removeReportMentor(report) {
      return await resources.reportMentor.removeReportMentor(report);
    },
    async loadStudentMentorPrimaryReports(config) {
      const res = await resources.studentMentorPrimaryReport.getStudentMentorPrimaryReports(config);
      if (res.__state === "success") {
        this.studentMentorReports = res.data.map(item => {
          return {
            ...item,
            report: item.reports[0]
          };
        });
      }
    },
    async createReportMentorPrimary(report) {
      return await resources.reportMentorPrimary.createReportMentorPrimary(report);
    },
    async updateReportMentorPrimary(report) {
      return await resources.reportMentorPrimary.updateReportMentor(report);
    },
    async removeReportMentorPrimary(report) {
      return await resources.reportMentorPrimary.removeReportMentorPrimary(report);
    },
    // CRUD для результатов по критериям MYP
    async loadReportSecondaryCriteria(config) {
      return await resources.reportSecondaryCriterion.getReportSecondaryCriteria(config);
    },
    async createReportSecondaryCriterion(report) {
      return await resources.reportSecondaryCriterion.createReportSecondaryCriterion(report);
    },
    async updateReportSecondaryCriterion(report) {
      return await resources.reportSecondaryCriterion.updateReportSecondaryCriterion(report);
    },
    async removeReportSecondaryCriterion(id) {
      return await resources.reportSecondaryCriterion.removeReportSecondaryCriterion(id);
    },
  }
});