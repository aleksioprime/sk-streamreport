import { CrudService } from "@/services/api/crud.service";

export class ReportExtraResource extends CrudService {
  constructor() {
    super("/api/report/extra");
  }

  getReportExtras() {
    return this.get();
  }

  createReportExtra(report) {
    return this.post(report);
  }

  updateReportExtra(report) {
    return this.patch(report);
  }

  removeReportExtra(id) {
    return this.delete(id);
  }
}