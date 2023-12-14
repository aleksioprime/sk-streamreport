import { CrudService } from "@/services/api/crud.service";

export class ReportTeacherSecondaryResource extends CrudService {
  constructor() {
    super("/api/report/teacher/secondary");
  }

  getReportTeachersSecondary(config) {
    return this.get(config);
  }

  createReportTeacherSecondary(report) {
    return this.post(report);
  }

  updateReportTeacherSecondary(report) {
    return this.patch(report);
  }

  removeReportTeacherSecondary(id) {
    return this.delete(id);
  }
}