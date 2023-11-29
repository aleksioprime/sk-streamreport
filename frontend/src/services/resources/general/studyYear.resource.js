import { CrudService } from "@/services/api/crud.service";

export class StudyYearResource extends CrudService {
  constructor() {
    super("/api/year/study");
  }

  getStudyYears() {
    return this.get();
  }
}