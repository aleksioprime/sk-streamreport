import { CrudService } from "@/services/api/crud.service";

export class CurriculumResource extends CrudService {
  constructor() {
    super("/api/curriculum");
  }

  getCurriculums() {
    return this.get();
  }

  retrieveCurriculum() {
    return this.retrieve(id);
  }
}