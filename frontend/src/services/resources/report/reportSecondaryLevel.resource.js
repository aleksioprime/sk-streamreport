import { CrudService } from "@/services/api/crud.service";

export class ReportSecondaryLevelResource extends CrudService {
  constructor() {
    super("/api/report/teacher/secondary/level");
  }

  getReportSecondaryLevels(config) {
    return this.get(config);
  }

  createReportSecondaryLevel(report) {
    return this.post(report);
  }

  updateReportSecondaryLevel(report) {
    return this.patch(report);
  }

  removeReportSecondaryLevel(id) {
    return this.delete(id);
  }
}