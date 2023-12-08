import { defineStore } from "pinia";

import resources from "@/services/resources";

export const usePortfolioStore = defineStore("portfolio", {
  state: () => ({
    eventParticipations: [],
  }),
  getters: {

  },
  actions: {
    async loadEventParticipations(config) {
      return await resources.eventParticipation.getEventParticipations(config);
    },
    async createEventParticipation(report) {
      return await resources.eventParticipation.createEventParticipation(report);
    },
    async updateEventParticipation(report) {
      return await resources.eventParticipation.updateEventParticipation(report);
    },
    async removeEventParticipation(report) {
      return await resources.eventParticipation.removeEventParticipation(report);
    },
  }
});