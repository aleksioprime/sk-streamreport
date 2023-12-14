import { CrudService } from "@/services/api/crud.service";

export class ReportMentorPrimaryUnitResource extends CrudService {
  constructor() {
    super("/api/report/mentor/primary/unit");
  }

  getReportMentorPrimaryUnits(config) {
    return this.get(config);
  }

  createReportMentorPrimaryUnit(report) {
    return this.post(report);
  }

  updateReportMentorPrimaryUnit(report) {
    return this.patch(report);
  }

  removeReportMentorPrimaryUnit(id) {
    return this.delete(id);
  }
}