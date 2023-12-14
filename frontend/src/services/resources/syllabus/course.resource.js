import { CrudService } from "@/services/api/crud.service";

export class CourseResource extends CrudService {
  constructor() {
    super("/api/syllabus/course");
  }

  getCourses(config) {
    return this.get(config);
  }
}