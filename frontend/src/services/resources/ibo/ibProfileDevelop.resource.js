import { CrudService } from "@/services/api/crud.service";

export class IbProfileDevelopResource extends CrudService {
  constructor() {
    super("/api/ib/unit/profile");
  }

  getIbProfileDevelops(config) {
    return this.get(config);
  }

  createIbProfileDevelop(data) {
    return this.post(data);
  }

  updateIbProfileDevelop(data) {
    return this.patch(data);
  }

  removeIbProfileDevelop(id) {
    return this.delete(id);
  }
}