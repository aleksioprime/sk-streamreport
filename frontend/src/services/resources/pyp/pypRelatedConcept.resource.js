import { CrudService } from "@/services/api/crud.service";

export class PypRelatedConceptResource extends CrudService {
  constructor() {
    super("/api/pyp/unit/relatedconcept");
  }

  getPypRelatedConcepts(config) {
    return this.get(config);
  }

  createPypRelatedConcept(report) {
    return this.post(report);
  }

  updatePypRelatedConcept(report) {
    return this.patch(report);
  }

  removePypRelatedConcept(id) {
    return this.delete(id);
  }
}