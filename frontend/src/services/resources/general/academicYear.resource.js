import { CrudService } from "@/services/api/crud.service";

export class AcademicYearResource extends CrudService {
  constructor() {
    super("/api/year/academic");
  }

  getAcademicYears() {
    return this.get();
  }
}