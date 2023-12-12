import { CrudService } from "@/services/api/crud.service";

export class PypAtlDevelopResource extends CrudService {
  constructor() {
    super("/api/pyp/unit/atl");
  }

  getPypAtlDevelops(config) {
    return this.get(config);
  }

  createPypAtlDevelop(report) {
    return this.post(report);
  }

  updatePypAtlDevelop(report) {
    return this.patch(report);
  }

  removePypAtlDevelop(id) {
    return this.delete(id);
  }
}