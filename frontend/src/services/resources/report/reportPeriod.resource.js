import { CrudService } from "@/services/api/crud.service";

export class ReportPeriodResource extends CrudService {
  constructor() {
    super("/api/report/period");
  }

  getReportPeriods() {
    return this.get();
  }
}