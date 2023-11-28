import { CrudService } from "@/services/api/crud.service";

export class GroupResource extends CrudService {
  constructor() {
    super("/api/group");
  }

  getGroups() {
    return this.get();
  }
}