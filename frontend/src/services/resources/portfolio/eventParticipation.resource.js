import { CrudService } from "@/services/api/crud.service";

export class EventParticipationResource extends CrudService {
  constructor() {
    super("/api/portfolio/event/participation");
  }

  getEventParticipations(config) {
    return this.get(config);
  }

  createEventParticipation(report) {
    return this.post(report);
  }

  updateEventParticipation(report) {
    return this.patch(report);
  }

  removeEventParticipation(id) {
    return this.delete(id);
  }
}