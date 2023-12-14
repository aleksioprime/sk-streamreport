import { CrudService } from "@/services/api/crud.service";

export class ObjectiveResource extends CrudService {
  constructor() {
    super("/api/myp/objective");
  }

  getObjectives(config) {
    return this.get(config);
  }
}