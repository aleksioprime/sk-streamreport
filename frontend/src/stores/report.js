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
        console.log('Получение периодов: ', this.reportPeriods)
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
            report: item.reportextra_student_reports[0] ?? null
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
    // CRUD для репортов учителя средней школы
    async loadReportTeachersSecondary(config) {
      const res = await resources.reportTeacherSecondary.getReportTeachersSecondary(config);
      if (res.__state === "success") {
        this.reportTeachers = res.data
        console.log('Получение репортов учителя средней школы: ', this.reportTeachers)
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
        console.log(res)
        this.studentMentorReports = res.data.map(item => {
          let report_teachers = []
          if (item.teacher_high_reports && item.teacher_high_reports.length) {
            report_teachers = [ ...item.teacher_high_reports ]
          } else if (item.teacher_secondary_reports && item.teacher_secondary_reports.length) {
            report_teachers = [ ...item.teacher_secondary_reports ]
          } else if (item.teacher_primary_reports && item.teacher_primary_reports.length) {
            report_teachers = [ ...item.teacher_primary_reports ]
          }
          return {
            ...item,
            report: item.reportmentor_student_reports[0] ?? null,
            report_extras: item.reportextra_student_reports,
            report_teachers: report_teachers
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
    // CRUD для репортов руководителя класса начальной школы
    async createReportMentorPrimary(report) {
      return await resources.reportMentorPrimary.createReportMentorPrimary(report);
    },
    async updateReportMentorPrimary(report) {
      return await resources.reportMentorPrimary.updateReportMentorPrimary(report);
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
    // CRUD для результатов по профилю студента IB
    async loadReportMentorIbProfiles(config) {
      return await resources.reportMentorIbProfile.getReportMentorIbProfiles(config);
    },
    async createReportMentorIbProfile(report) {
      return await resources.reportMentorIbProfile.createReportMentorIbProfile(report);
    },
    async updateReportMentorIbProfile(report) {
      return await resources.reportMentorIbProfile.updateReportMentorIbProfile(report);
    },
    async removeReportMentorIbProfile(id) {
      return await resources.reportMentorIbProfile.removeReportMentorIbProfile(id);
    },
    // CRUD для результатов по критериям MYP
    async loadReportSecondaryLevels(config) {
      return await resources.reportSecondaryLevel.getReportSecondaryLevels(config);
    },
    async createReportSecondaryLevel(report) {
      return await resources.reportSecondaryLevel.createReportSecondaryLevel(report);
    },
    async updateReportSecondaryLevel(report) {
      return await resources.reportSecondaryLevel.updateReportSecondaryLevel(report);
    },
    async removeReportSecondaryLevel(id) {
      return await resources.reportSecondaryLevel.removeReportSecondaryLevel(id);
    },
  }
});