import { CrudService } from "@/services/api/crud.service";

export class StudyYearResource extends CrudService {
  constructor() {
    super("/api/year/study");
  }

  getStudyYears(config) {
    return this.get(config);
  }
}