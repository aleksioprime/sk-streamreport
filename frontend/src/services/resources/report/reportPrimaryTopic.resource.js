import { CrudService } from "@/services/api/crud.service";

export class ReportPrimaryTopicResource extends CrudService {
  constructor() {
    super("/api/report/teacher/primary/topic");
  }

  getReportPrimaryTopics(config) {
    return this.get(config);
  }

  createReportPrimaryTopic(report) {
    return this.post(report);
  }

  updateReportPrimaryTopic(report) {
    return this.patch(report);
  }

  removeReportPrimaryTopic(id) {
    return this.delete(id);
  }
}