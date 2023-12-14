import { CrudService } from "@/services/api/crud.service";

export class ReportTeacherPrimaryResource extends CrudService {
  constructor() {
    super("/api/report/teacher/primary");
  }

  getReportTeachersPrimary(config) {
    return this.get(config);
  }

  createReportTeacherPrimary(report) {
    return this.post(report);
  }

  updateReportTeacherPrimary(report) {
    return this.patch(report);
  }

  removeReportTeacherPrimary(id) {
    return this.delete(id);
  }
}