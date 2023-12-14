import { CrudService } from "@/services/api/crud.service";

export class StrandResource extends CrudService {
  constructor() {
    super("/api/myp/strand");
  }

  getStrands(config) {
    return this.get(config);
  }
}