import { CrudService } from "@/services/api/crud.service";

export class StudentExtraReportResource extends CrudService {
  constructor() {
    super("/api/report/student");
  }

  getStudentExtraReports(config) {
    return this.get(config);
  }
}