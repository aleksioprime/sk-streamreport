import { CrudService } from "@/services/api/crud.service";

export class TeachingLoadResource extends CrudService {
  constructor() {
    super("/api/curriculum/teaching");
  }

  getTeachingLoads(config) {
    return this.get(config);
  }

  createTeachingLoad(data) {
    return this.post(data);
  }

  updateTeachingLoad(data) {
    return this.patch(data);
  }

  removeTeachingLoad(id) {
    return this.delete(id);
  }
}