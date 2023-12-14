import { CrudService } from "@/services/api/crud.service";

export class ReportMentorPrimaryResource extends CrudService {
  constructor() {
    super("/api/report/mentor/primary");
  }

  getReportsMentorPrimary(config) {
    return this.get(config);
  }

  createReportMentorPrimary(report) {
    return this.post(report);
  }

  updateReportMentorPrimary(report) {
    return this.patch(report);
  }

  removeReportMentorPrimary(id) {
    return this.delete(id);
  }
}