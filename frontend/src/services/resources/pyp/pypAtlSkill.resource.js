import { CrudService } from "@/services/api/crud.service";

export class PypAtlSkillResource extends CrudService {
  constructor() {
    super("/api/pyp/atl/skill");
  }

  getPypAtlSkills(config) {
    return this.get(config);
  }
}