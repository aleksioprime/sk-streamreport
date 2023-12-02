import { CrudService } from "@/services/api/crud.service";

export class LearnerProfileResource extends CrudService {
  constructor() {
    super("/api/ib/profile");
  }

  getLearnerProfiles(config) {
    return this.get(config);
  }
}