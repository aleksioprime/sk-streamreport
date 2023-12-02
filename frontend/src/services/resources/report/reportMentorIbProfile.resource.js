import { CrudService } from "@/services/api/crud.service";

export class ReportMentorIbProfileResource extends CrudService {
  constructor() {
    super("/api/report/mentor/ibprofile");
  }

  getReportMentorIbProfiles(config) {
    return this.get(config);
  }

  createReportMentorIbProfile(report) {
    return this.post(report);
  }

  updateReportMentorIbProfile(report) {
    return this.patch(report);
  }

  removeReportMentorIbProfile(id) {
    return this.delete(id);
  }
}