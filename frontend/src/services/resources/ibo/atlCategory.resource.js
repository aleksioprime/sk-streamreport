import { CrudService } from "@/services/api/crud.service";

export class AtlCategoryResource extends CrudService {
  constructor() {
    super("/api/ib/atl/category");
  }

  getAtlCategories(config) {
    return this.get(config);
  }
}