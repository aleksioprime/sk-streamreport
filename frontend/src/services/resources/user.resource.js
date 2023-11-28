import { CrudService } from "@/services/api/crud.service";

export class UserResource extends CrudService {
  constructor() {
    super("/api/user");
  }

  getUsers() {
    return this.get();
  }

  createUser(user) {
    return this.post(user);
  }

  partialUpdateUser(user) {
    return this.patch(user);
  }

  updateUser(user) {
    return this.put(user);
  }

  updateUserPhoto(userId, photo) {
    const formData = new FormData();
    formData.append('photo', photo);

    return this.$post(`${this.resource}/${userId}/photo`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}