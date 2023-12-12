import { CrudService } from "@/services/api/crud.service";

export class PypLinesOfInquiryResource extends CrudService {
  constructor() {
    super("/api/pyp/unit/inquiry");
  }

  getPypLinesOfInquiries(config) {
    return this.get(config);
  }

  createPypLinesOfInquiry(report) {
    return this.post(report);
  }

  updatePypLinesOfInquiry(report) {
    return this.patch(report);
  }

  removePypLinesOfInquiry(id) {
    return this.delete(id);
  }
}