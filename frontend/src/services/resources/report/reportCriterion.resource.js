import { CrudService } from "@/services/api/crud.service";

export class ReportCriterionResource extends CrudService {
  constructor() {
    super("/api/report/criterion");
  }

  getReportCriteria(config) {
    return this.get(config);
  }
}