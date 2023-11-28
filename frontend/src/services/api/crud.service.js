import { ApiService } from "@/services/api/api.service";

export class CrudService extends ApiService {
  constructor(resource) {
    super();
    this.resource = resource;
  }

  get() {
    return this.$get(this.resource);
  }

  retrieve(id) {
    return this.$get(`${this.resource}/${id}`);
  }

  post(entity) {
    return this.$post(this.resource, entity);
  }

  put(entity) {
    return this.$put(`${this.resource}/${entity.id}`, entity);
  }

  patch(entity) {
    return this.$patch(`${this.resource}/${entity.id}`, entity);
  }

  delete(id) {
    return this.$delete(`${this.resource}/${id}`);
  }
}
