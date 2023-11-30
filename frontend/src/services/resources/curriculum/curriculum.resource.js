import { CrudService } from "@/services/api/crud.service";

export class CurriculumResource extends CrudService {
  constructor() {
    super("/api/curriculum");
  }

  getCurriculums(config) {
    return this.get(config);
  }

  retrieveCurriculum(id) {
    return this.retrieve(id);
  }
}