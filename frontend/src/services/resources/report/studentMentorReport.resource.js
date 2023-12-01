import { CrudService } from "@/services/api/crud.service";

export class StudentMentorReportResource extends CrudService {
  constructor() {
    super("/api/report/mentor/student");
  }

  getStudentMentorReports(config) {
    return this.get(config);
  }
}