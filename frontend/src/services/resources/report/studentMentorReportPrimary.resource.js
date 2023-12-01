import { CrudService } from "@/services/api/crud.service";

export class StudentMentorReportPrimaryResource extends CrudService {
  constructor() {
    super("/api/report/mentor/primary/student");
  }

  getStudentMentorPrimaryReports(config) {
    return this.get(config);
  }
}