import { defineStore } from "pinia";

import resources from "@/services/resources";

export const useGeneralStore = defineStore("general", {
  state: () => ({
    studyYears: [],
    academicYears: [],
    groups: [],
    users: [],
  }),
  getters: {
    isStudyYearsLoaded() {
      return (
        this.studyYears.length > 0
      );
    },
    isAcademicYearsLoaded() {
      return (
        this.academicYears.length > 0
      );
    },
    isGroupsLoaded() {
      return (
        this.groups.length > 0
      );
    },
    relevantYear() {
      // Сортировка периодов по дате начала
      this.academicYears.sort((a, b) => new Date(a.date_start) - new Date(b.date_start));
      let lastPeriod = null;
      const currentDate = new Date();
    
      for (const period of this.academicYears) {
        const startDate = new Date(period.date_start);
        const endDate = new Date(period.date_end);
    
        // Проверка, входит ли текущая дата в период
        if (startDate <= currentDate && currentDate <= endDate) {
          return period;
        }
    
        // Обновление последнего периода, который закончился до текущей даты
        if (endDate < currentDate) {
          lastPeriod = period;
        }
      }
      // Возврат последнего периода, если текущая дата не входит ни в один из периодов
      return lastPeriod;
    }
  },
  actions: {
    async loadStudyYears(config) {
      const res = await resources.studyYear.getStudyYears(config);
      if (res.__state === "success") {
        this.studyYears = res.data.map(item => {
          return {
            ...item, // Копирование всех существующих свойств
            // name: item.number + ' классы' // Добавление нового свойства name
          };
        });
        console.log('Получение учебных параллелей: ', this.studyYears)
      }
    },
    async loadAcademicYears() {
      const res = await resources.academicYear.getAcademicYears();
      if (res.__state === "success") {
        this.academicYears = res.data
        console.log('Получение учебных лет: ', this.academicYears)
      }
    },
    async loadGroups(config) {
      const res = await resources.group.getGroups(config);
      if (res.__state === "success") {
        this.groups = res.data.map(item => {
          return {
            ...item, // Копирование всех существующих свойств
            full_name: item.name + ' класс' // Добавление нового свойства name
          };
        });
        console.log('Получение классов: ', this.groups)
      }
    },
    async loadUsers(config) {
      const res = await resources.user.getUsers(config);
      if (res.__state === "success") {
        this.users = res.data
        console.log('Получение пользователей: ', this.users)
      }
    },
  }
});