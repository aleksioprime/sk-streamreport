import { CrudService } from "@/services/api/crud.service";

export class UnitReflectionPostResource extends CrudService {
  constructor() {
    super("/api/ib/unit/reflection");
  }

  getUnitReflectionPosts(config) {
    return this.get(config);
  }

  createUnitReflectionPost(data) {
    return this.post(data);
  }

  updateUnitReflectionPost(data) {
    return this.patch(data);
  }

  removeUnitReflectionPost(id) {
    return this.delete(id);
  }
}