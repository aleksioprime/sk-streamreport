import { CrudService } from "@/services/api/crud.service";

export class ReportMentorResource extends CrudService {
  constructor() {
    super("/api/report/mentor");
  }

  getReportsMentor() {
    return this.get();
  }

  createReportMentor(report) {
    return this.post(report);
  }

  // exportReportMentor(id, config) {
  //   return this.$get(`${this.resource}/${id}/export`, config);
  // }

  updateReportMentor(report) {
    return this.patch(report);
  }

  removeReportMentor(id) {
    return this.delete(id);
  }
}