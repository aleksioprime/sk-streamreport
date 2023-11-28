import { AuthResource } from "@/services/resources/auth.resource";
import { UserResource } from "@/services/resources/user.resource";

export default {
    auth: new AuthResource(),
    user: new UserResource(),
  };