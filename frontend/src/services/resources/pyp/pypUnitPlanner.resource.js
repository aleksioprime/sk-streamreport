import { CrudService } from "@/services/api/crud.service";

export class PypUnitPlannerResource extends CrudService {
  constructor() {
    super("/api/pyp/unit");
  }

  getPypUnitPlanners(config) {
    return this.get(config);
  }

  retrievePypUnitPlanner(id) {
    return this.retrieve(id);
  }

  createPypUnitPlanner(report) {
    return this.post(report);
  }

  updatePypUnitPlanner(report) {
    return this.patch(report);
  }

  removePypUnitPlanner(id) {
    return this.delete(id);
  }
}