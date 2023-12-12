import { CrudService } from "@/services/api/crud.service";

export class PypKeyConceptResource extends CrudService {
  constructor() {
    super("/api/pyp/keyconcept");
  }

  getPypKeyConcepts(config) {
    return this.get(config);
  }
}