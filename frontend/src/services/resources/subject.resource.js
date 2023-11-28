import { CrudService } from "@/services/api/crud.service";

export class SubjectResource extends CrudService {
  constructor() {
    super("/api/subject");
  }

  getSubjects() {
    return this.get();
  }
}