import { CrudService } from "@/services/api/crud.service";

export class TransdisciplinaryThemeResource extends CrudService {
  constructor() {
    super("/api/pyp/transdisciplinary");
  }

  getTransdisciplinaryThemes(config) {
    return this.get(config);
  }
}