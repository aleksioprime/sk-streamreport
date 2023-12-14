import axios from "axios";
import { ApiService } from "@/services/api/api.service";

export class AuthService extends ApiService {
  constructor(path) {
    super();
    this.path = path;
  }

  setAuthHeader(token) {
    axios.defaults.headers.common["Authorization"] = token
      ? `Bearer ${token}`
      : "";
  }

  login(params) {
    return this.$post(`${this.path}/token/`, params);
  }

  refresh(params) {
    return this.$post(`${this.path}/token/refresh/`, params);
  }

  logout() {
    return this.$delete(`${this.path}/logout/`);
  }

  whoami() {
    return this.$get(`${this.path}/user/me`);
  }
}