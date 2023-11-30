import { CrudService } from "@/services/api/crud.service";

export class ReportTeacherHighResource extends CrudService {
  constructor() {
    super("/api/report/teacher/high");
  }

  getReportTeachersHigh(config) {
    return this.get(config);
  }

  createReportTeacherHigh(report) {
    return this.post(report);
  }

  updateReportTeacherHigh(report) {
    return this.patch(report);
  }

  removeReportTeacherHigh(id) {
    return this.delete(id);
  }
}