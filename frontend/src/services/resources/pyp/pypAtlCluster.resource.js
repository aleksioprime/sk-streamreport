import { CrudService } from "@/services/api/crud.service";

export class PypAtlClusterResource extends CrudService {
  constructor() {
    super("/api/pyp/atl/cluster");
  }

  getPypAtlClusters(config) {
    return this.get(config);
  }
}