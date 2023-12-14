import { CrudService } from "@/services/api/crud.service";

export class ReportSecondaryCriterionResource extends CrudService {
  constructor() {
    super("/api/report/teacher/secondary/criterion");
  }

  getReportSecondaryCriteria(config) {
    return this.get(config);
  }

  createReportSecondaryCriterion(report) {
    return this.post(report);
  }

  updateReportSecondaryCriterion(report) {
    return this.patch(report);
  }

  removeReportSecondaryCriterion(id) {
    return this.delete(id);
  }
}