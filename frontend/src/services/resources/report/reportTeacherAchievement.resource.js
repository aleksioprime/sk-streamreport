import { CrudService } from "@/services/api/crud.service";

export class ReportTeacherAchievementResource extends CrudService {
  constructor() {
    super("/api/report/teacher/achievement");
  }

  getReportTeacherAchievements(config) {
    return this.get(config);
  }

  createReportTeacherAchievement(report) {
    return this.post(report);
  }

  updateReportTeacherAchievement(report) {
    return this.patch(report);
  }

  removeReportTeacherAchievement(id) {
    return this.delete(id);
  }
}